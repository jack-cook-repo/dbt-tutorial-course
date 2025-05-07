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
from collections import OrderedDict
import functools
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.cloud.pubsublite_v1.types import common
from google.cloud.pubsublite_v1.types import topic_stats
from cloudsdk.google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import TopicStatsServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import TopicStatsServiceGrpcAsyncIOTransport
from .client import TopicStatsServiceClient


class TopicStatsServiceAsyncClient:
    """This service allows users to get stats about messages in
    their topic.
    """

    _client: TopicStatsServiceClient

    DEFAULT_ENDPOINT = TopicStatsServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = TopicStatsServiceClient.DEFAULT_MTLS_ENDPOINT

    topic_path = staticmethod(TopicStatsServiceClient.topic_path)
    parse_topic_path = staticmethod(TopicStatsServiceClient.parse_topic_path)
    common_billing_account_path = staticmethod(
        TopicStatsServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        TopicStatsServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(TopicStatsServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        TopicStatsServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        TopicStatsServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        TopicStatsServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(TopicStatsServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        TopicStatsServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(TopicStatsServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        TopicStatsServiceClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            TopicStatsServiceAsyncClient: The constructed client.
        """
        return TopicStatsServiceClient.from_service_account_info.__func__(TopicStatsServiceAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            TopicStatsServiceAsyncClient: The constructed client.
        """
        return TopicStatsServiceClient.from_service_account_file.__func__(TopicStatsServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return TopicStatsServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> TopicStatsServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            TopicStatsServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(TopicStatsServiceClient).get_transport_class, type(TopicStatsServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, TopicStatsServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the topic stats service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.TopicStatsServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = TopicStatsServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def compute_message_stats(
        self,
        request: Union[topic_stats.ComputeMessageStatsRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> topic_stats.ComputeMessageStatsResponse:
        r"""Compute statistics about a range of messages in a
        given topic and partition.

        Args:
            request (Union[google.cloud.pubsublite_v1.types.ComputeMessageStatsRequest, dict]):
                The request object. Compute statistics about a range of
                messages in a given topic and partition.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.pubsublite_v1.types.ComputeMessageStatsResponse:
                Response containing stats for
                messages in the requested topic and
                partition.

        """
        # Create or coerce a protobuf request object.
        request = topic_stats.ComputeMessageStatsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.compute_message_stats,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("topic", request.topic),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def compute_head_cursor(
        self,
        request: Union[topic_stats.ComputeHeadCursorRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> topic_stats.ComputeHeadCursorResponse:
        r"""Compute the head cursor for the partition.
        The head cursor's offset is guaranteed to be less than
        or equal to all messages which have not yet been
        acknowledged as published, and greater than the offset
        of any message whose publish has already been
        acknowledged. It is zero if there have never been
        messages in the partition.

        Args:
            request (Union[google.cloud.pubsublite_v1.types.ComputeHeadCursorRequest, dict]):
                The request object. Compute the current head cursor for
                a partition.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.pubsublite_v1.types.ComputeHeadCursorResponse:
                Response containing the head cursor
                for the requested topic and partition.

        """
        # Create or coerce a protobuf request object.
        request = topic_stats.ComputeHeadCursorRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.compute_head_cursor,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("topic", request.topic),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def compute_time_cursor(
        self,
        request: Union[topic_stats.ComputeTimeCursorRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> topic_stats.ComputeTimeCursorResponse:
        r"""Compute the corresponding cursor for a publish or
        event time in a topic partition.

        Args:
            request (Union[google.cloud.pubsublite_v1.types.ComputeTimeCursorRequest, dict]):
                The request object. Compute the corresponding cursor for
                a publish or event time in a topic partition.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.pubsublite_v1.types.ComputeTimeCursorResponse:
                Response containing the cursor
                corresponding to a publish or event time
                in a topic partition.

        """
        # Create or coerce a protobuf request object.
        request = topic_stats.ComputeTimeCursorRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.compute_time_cursor,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("topic", request.topic),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-pubsublite",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("TopicStatsServiceAsyncClient",)
