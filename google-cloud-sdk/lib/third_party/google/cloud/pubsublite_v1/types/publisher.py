# -*- coding: utf-8 -*-
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
#
import proto  # type: ignore

from google.cloud.pubsublite_v1.types import common


__protobuf__ = proto.module(
    package="google.cloud.pubsublite.v1",
    manifest={
        "InitialPublishRequest",
        "InitialPublishResponse",
        "MessagePublishRequest",
        "MessagePublishResponse",
        "PublishRequest",
        "PublishResponse",
    },
)


class InitialPublishRequest(proto.Message):
    r"""The first request that must be sent on a newly-opened stream.

    Attributes:
        topic (str):
            The topic to which messages will be written.
        partition (int):
            The partition within the topic to which messages will be
            written. Partitions are zero indexed, so ``partition`` must
            be in the range [0, topic.num_partitions).
    """

    topic = proto.Field(proto.STRING, number=1,)
    partition = proto.Field(proto.INT64, number=2,)


class InitialPublishResponse(proto.Message):
    r"""Response to an InitialPublishRequest.
    """


class MessagePublishRequest(proto.Message):
    r"""Request to publish messages to the topic.

    Attributes:
        messages (Sequence[google.cloud.pubsublite_v1.types.PubSubMessage]):
            The messages to publish.
    """

    messages = proto.RepeatedField(
        proto.MESSAGE, number=1, message=common.PubSubMessage,
    )


class MessagePublishResponse(proto.Message):
    r"""Response to a MessagePublishRequest.

    Attributes:
        start_cursor (google.cloud.pubsublite_v1.types.Cursor):
            The cursor of the first published message in
            the batch. The cursors for any remaining
            messages in the batch are guaranteed to be
            sequential.
    """

    start_cursor = proto.Field(proto.MESSAGE, number=1, message=common.Cursor,)


class PublishRequest(proto.Message):
    r"""Request sent from the client to the server on a stream.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        initial_request (google.cloud.pubsublite_v1.types.InitialPublishRequest):
            Initial request on the stream.

            This field is a member of `oneof`_ ``request_type``.
        message_publish_request (google.cloud.pubsublite_v1.types.MessagePublishRequest):
            Request to publish messages.

            This field is a member of `oneof`_ ``request_type``.
    """

    initial_request = proto.Field(
        proto.MESSAGE, number=1, oneof="request_type", message="InitialPublishRequest",
    )
    message_publish_request = proto.Field(
        proto.MESSAGE, number=2, oneof="request_type", message="MessagePublishRequest",
    )


class PublishResponse(proto.Message):
    r"""Response to a PublishRequest.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        initial_response (google.cloud.pubsublite_v1.types.InitialPublishResponse):
            Initial response on the stream.

            This field is a member of `oneof`_ ``response_type``.
        message_response (google.cloud.pubsublite_v1.types.MessagePublishResponse):
            Response to publishing messages.

            This field is a member of `oneof`_ ``response_type``.
    """

    initial_response = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="response_type",
        message="InitialPublishResponse",
    )
    message_response = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="response_type",
        message="MessagePublishResponse",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
