# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
from typing import Optional, List

from overrides import overrides
import logging
from google.cloud.pubsub_v1.types import BatchSettings

from google.cloud.pubsublite.internal.wait_ignore_cancelled import wait_ignore_errors
from google.cloud.pubsublite.internal.wire.publisher import Publisher
from google.cloud.pubsublite.internal.wire.retrying_connection import (
    RetryingConnection,
    ConnectionFactory,
)
from google.api_core.exceptions import FailedPrecondition, GoogleAPICallError
from google.cloud.pubsublite.internal.wire.connection_reinitializer import (
    ConnectionReinitializer,
)
from google.cloud.pubsublite.internal.wire.connection import Connection
from google.cloud.pubsublite.internal.wire.serial_batcher import (
    SerialBatcher,
    RequestSizer,
    BatchSize,
)
from google.cloud.pubsublite.types import Partition, MessageMetadata
from google.cloud.pubsublite_v1.types import (
    PubSubMessage,
    Cursor,
    PublishRequest,
    PublishResponse,
    InitialPublishRequest,
)
from google.cloud.pubsublite.internal.wire.work_item import WorkItem

_LOGGER = logging.getLogger(__name__)

# Maximum bytes per batch at 3.5 MiB to avoid GRPC limit of 4 MiB
_MAX_BYTES = int(3.5 * 1024 * 1024)

# Maximum messages per batch at 1000
_MAX_MESSAGES = 1000


class SinglePartitionPublisher(
    Publisher,
    ConnectionReinitializer[PublishRequest, PublishResponse],
    RequestSizer[PubSubMessage],
):
    _initial: InitialPublishRequest
    _batching_settings: BatchSettings
    _connection: RetryingConnection[PublishRequest, PublishResponse]

    _batcher: SerialBatcher[PubSubMessage, Cursor]
    _outstanding_writes: List[List[WorkItem[PubSubMessage, Cursor]]]

    _receiver: Optional[asyncio.Future]
    _flusher: Optional[asyncio.Future]

    def __init__(
        self,
        initial: InitialPublishRequest,
        batching_settings: BatchSettings,
        factory: ConnectionFactory[PublishRequest, PublishResponse],
    ):
        self._initial = initial
        self._batching_settings = batching_settings
        self._connection = RetryingConnection(factory, self)
        self._batcher = SerialBatcher(self)
        self._outstanding_writes = []
        self._receiver = None
        self._flusher = None

    @property
    def _partition(self) -> Partition:
        return Partition(self._initial.partition)

    async def __aenter__(self):
        await self._connection.__aenter__()
        return self

    def _start_loopers(self):
        assert self._receiver is None
        assert self._flusher is None
        self._receiver = asyncio.ensure_future(self._receive_loop())
        self._flusher = asyncio.ensure_future(self._flush_loop())

    async def _stop_loopers(self):
        if self._receiver:
            self._receiver.cancel()
            await wait_ignore_errors(self._receiver)
            self._receiver = None
        if self._flusher:
            self._flusher.cancel()
            await wait_ignore_errors(self._flusher)
            self._flusher = None

    def _handle_response(self, response: PublishResponse):
        if "message_response" not in response:
            self._connection.fail(
                FailedPrecondition(
                    "Received an invalid subsequent response on the publish stream."
                )
            )
        if not self._outstanding_writes:
            self._connection.fail(
                FailedPrecondition(
                    "Received an publish response on the stream with no outstanding publishes."
                )
            )
        next_offset: Cursor = response.message_response.start_cursor.offset
        batch: List[WorkItem[PubSubMessage]] = self._outstanding_writes.pop(0)
        for item in batch:
            item.response_future.set_result(Cursor(offset=next_offset))
            next_offset += 1

    async def _receive_loop(self):
        while True:
            response = await self._connection.read()
            self._handle_response(response)

    async def _flush_loop(self):
        while True:
            await asyncio.sleep(self._batching_settings.max_latency)
            await self._flush()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._connection.error():
            self._fail_if_retrying_failed()
        else:
            await self._flush()
        await self._stop_loopers()
        await self._connection.__aexit__(exc_type, exc_val, exc_tb)

    def _fail_if_retrying_failed(self):
        if self._connection.error():
            for batch in self._outstanding_writes:
                for item in batch:
                    item.response_future.set_exception(self._connection.error())

    async def _flush(self):
        batch = self._batcher.flush()
        if not batch:
            return
        self._outstanding_writes.append(batch)
        aggregate = PublishRequest()
        aggregate.message_publish_request.messages = [item.request for item in batch]
        try:
            await self._connection.write(aggregate)
        except GoogleAPICallError as e:
            _LOGGER.debug(f"Failed publish on stream: {e}")
            self._fail_if_retrying_failed()

    async def publish(self, message: PubSubMessage) -> MessageMetadata:
        future = self._batcher.add(message)
        if self._should_flush():
            await self._flush()
        return MessageMetadata(self._partition, await future)

    @overrides
    async def stop_processing(self, error: GoogleAPICallError):
        await self._stop_loopers()

    @overrides
    async def reinitialize(
        self, connection: Connection[PublishRequest, PublishResponse],
    ):
        await connection.write(PublishRequest(initial_request=self._initial))
        response = await connection.read()
        if "initial_response" not in response:
            self._connection.fail(
                FailedPrecondition(
                    "Received an invalid initial response on the publish stream."
                )
            )
        for batch in self._outstanding_writes:
            aggregate = PublishRequest()
            aggregate.message_publish_request.messages = [
                item.request for item in batch
            ]
            await connection.write(aggregate)
        self._start_loopers()

    @overrides
    def get_size(self, request: PubSubMessage) -> BatchSize:
        return BatchSize(
            element_count=1, byte_count=PubSubMessage.pb(request).ByteSize()
        )

    def _should_flush(self) -> bool:
        size = self._batcher.size()
        return (size.element_count >= self._batching_settings.max_messages) or (
            size.byte_count >= self._batching_settings.max_bytes
        )
