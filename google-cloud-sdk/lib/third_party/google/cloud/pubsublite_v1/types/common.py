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

from cloudsdk.google.protobuf import duration_pb2  # type: ignore
from cloudsdk.google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.pubsublite.v1",
    manifest={
        "AttributeValues",
        "PubSubMessage",
        "Cursor",
        "SequencedMessage",
        "Reservation",
        "Topic",
        "Subscription",
        "TimeTarget",
    },
)


class AttributeValues(proto.Message):
    r"""The values associated with a key of an attribute.

    Attributes:
        values (Sequence[bytes]):
            The list of values associated with a key.
    """

    values = proto.RepeatedField(proto.BYTES, number=1,)


class PubSubMessage(proto.Message):
    r"""A message that is published by publishers and delivered to
    subscribers.

    Attributes:
        key (bytes):
            The key used for routing messages to
            partitions or for compaction (e.g., keep the
            last N messages per key). If the key is empty,
            the message is routed to an arbitrary partition.
        data (bytes):
            The payload of the message.
        attributes (Sequence[google.cloud.pubsublite_v1.types.PubSubMessage.AttributesEntry]):
            Optional attributes that can be used for
            message metadata/headers.
        event_time (google.protobuf.timestamp_pb2.Timestamp):
            An optional, user-specified event time.
    """

    key = proto.Field(proto.BYTES, number=1,)
    data = proto.Field(proto.BYTES, number=2,)
    attributes = proto.MapField(
        proto.STRING, proto.MESSAGE, number=3, message="AttributeValues",
    )
    event_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)


class Cursor(proto.Message):
    r"""A cursor that describes the position of a message within a
    topic partition.

    Attributes:
        offset (int):
            The offset of a message within a topic
            partition. Must be greater than or equal 0.
    """

    offset = proto.Field(proto.INT64, number=1,)


class SequencedMessage(proto.Message):
    r"""A message that has been stored and sequenced by the Pub/Sub
    Lite system.

    Attributes:
        cursor (google.cloud.pubsublite_v1.types.Cursor):
            The position of a message within the
            partition where it is stored.
        publish_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the message was received by the
            server when it was first published.
        message (google.cloud.pubsublite_v1.types.PubSubMessage):
            The user message.
        size_bytes (int):
            The size in bytes of this message for flow
            control and quota purposes.
    """

    cursor = proto.Field(proto.MESSAGE, number=1, message="Cursor",)
    publish_time = proto.Field(
        proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,
    )
    message = proto.Field(proto.MESSAGE, number=3, message="PubSubMessage",)
    size_bytes = proto.Field(proto.INT64, number=4,)


class Reservation(proto.Message):
    r"""Metadata about a reservation resource.

    Attributes:
        name (str):
            The name of the reservation. Structured like:
            projects/{project_number}/locations/{location}/reservations/{reservation_id}
        throughput_capacity (int):
            The reserved throughput capacity. Every unit
            of throughput capacity is equivalent to 1 MiB/s
            of published messages or 2 MiB/s of subscribed
            messages.

            Any topics which are declared as using capacity
            from a Reservation will consume resources from
            this reservation instead of being charged
            individually.
    """

    name = proto.Field(proto.STRING, number=1,)
    throughput_capacity = proto.Field(proto.INT64, number=2,)


class Topic(proto.Message):
    r"""Metadata about a topic resource.

    Attributes:
        name (str):
            The name of the topic. Structured like:
            projects/{project_number}/locations/{location}/topics/{topic_id}
        partition_config (google.cloud.pubsublite_v1.types.Topic.PartitionConfig):
            The settings for this topic's partitions.
        retention_config (google.cloud.pubsublite_v1.types.Topic.RetentionConfig):
            The settings for this topic's message
            retention.
        reservation_config (google.cloud.pubsublite_v1.types.Topic.ReservationConfig):
            The settings for this topic's Reservation
            usage.
    """

    class PartitionConfig(proto.Message):
        r"""The settings for a topic's partitions.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            count (int):
                The number of partitions in the topic. Must be at least 1.

                Once a topic has been created the number of partitions can
                be increased but not decreased. Message ordering is not
                guaranteed across a topic resize. For more information see
                https://cloud.google.com/pubsub/lite/docs/topics#scaling_capacity
            scale (int):
                DEPRECATED: Use capacity instead which can express a
                superset of configurations.

                Every partition in the topic is allocated throughput
                equivalent to ``scale`` times the standard partition
                throughput (4 MiB/s). This is also reflected in the cost of
                this topic; a topic with ``scale`` of 2 and count of 10 is
                charged for 20 partitions. This value must be in the range
                [1,4].

                This field is a member of `oneof`_ ``dimension``.
            capacity (google.cloud.pubsublite_v1.types.Topic.PartitionConfig.Capacity):
                The capacity configuration.

                This field is a member of `oneof`_ ``dimension``.
        """

        class Capacity(proto.Message):
            r"""The throughput capacity configuration for each partition.

            Attributes:
                publish_mib_per_sec (int):
                    Publish throughput capacity per partition in
                    MiB/s. Must be >= 4 and <= 16.
                subscribe_mib_per_sec (int):
                    Subscribe throughput capacity per partition
                    in MiB/s. Must be >= 4 and <= 32.
            """

            publish_mib_per_sec = proto.Field(proto.INT32, number=1,)
            subscribe_mib_per_sec = proto.Field(proto.INT32, number=2,)

        count = proto.Field(proto.INT64, number=1,)
        scale = proto.Field(proto.INT32, number=2, oneof="dimension",)
        capacity = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="dimension",
            message="Topic.PartitionConfig.Capacity",
        )

    class RetentionConfig(proto.Message):
        r"""The settings for a topic's message retention.

        Attributes:
            per_partition_bytes (int):
                The provisioned storage, in bytes, per partition. If the
                number of bytes stored in any of the topic's partitions
                grows beyond this value, older messages will be dropped to
                make room for newer ones, regardless of the value of
                ``period``.
            period (google.protobuf.duration_pb2.Duration):
                How long a published message is retained. If unset, messages
                will be retained as long as the bytes retained for each
                partition is below ``per_partition_bytes``.
        """

        per_partition_bytes = proto.Field(proto.INT64, number=1,)
        period = proto.Field(proto.MESSAGE, number=2, message=duration_pb2.Duration,)

    class ReservationConfig(proto.Message):
        r"""The settings for this topic's Reservation usage.

        Attributes:
            throughput_reservation (str):
                The Reservation to use for this topic's throughput capacity.
                Structured like:
                projects/{project_number}/locations/{location}/reservations/{reservation_id}
        """

        throughput_reservation = proto.Field(proto.STRING, number=1,)

    name = proto.Field(proto.STRING, number=1,)
    partition_config = proto.Field(proto.MESSAGE, number=2, message=PartitionConfig,)
    retention_config = proto.Field(proto.MESSAGE, number=3, message=RetentionConfig,)
    reservation_config = proto.Field(
        proto.MESSAGE, number=4, message=ReservationConfig,
    )


class Subscription(proto.Message):
    r"""Metadata about a subscription resource.

    Attributes:
        name (str):
            The name of the subscription. Structured like:
            projects/{project_number}/locations/{location}/subscriptions/{subscription_id}
        topic (str):
            The name of the topic this subscription is attached to.
            Structured like:
            projects/{project_number}/locations/{location}/topics/{topic_id}
        delivery_config (google.cloud.pubsublite_v1.types.Subscription.DeliveryConfig):
            The settings for this subscription's message
            delivery.
    """

    class DeliveryConfig(proto.Message):
        r"""The settings for a subscription's message delivery.

        Attributes:
            delivery_requirement (google.cloud.pubsublite_v1.types.Subscription.DeliveryConfig.DeliveryRequirement):
                The DeliveryRequirement for this
                subscription.
        """

        class DeliveryRequirement(proto.Enum):
            r"""When this subscription should send messages to subscribers relative
            to messages persistence in storage. For details, see `Creating Lite
            subscriptions <https://cloud.google.com/pubsub/lite/docs/subscriptions#creating_lite_subscriptions>`__.
            """
            DELIVERY_REQUIREMENT_UNSPECIFIED = 0
            DELIVER_IMMEDIATELY = 1
            DELIVER_AFTER_STORED = 2

        delivery_requirement = proto.Field(
            proto.ENUM,
            number=3,
            enum="Subscription.DeliveryConfig.DeliveryRequirement",
        )

    name = proto.Field(proto.STRING, number=1,)
    topic = proto.Field(proto.STRING, number=2,)
    delivery_config = proto.Field(proto.MESSAGE, number=3, message=DeliveryConfig,)


class TimeTarget(proto.Message):
    r"""A target publish or event time. Can be used for seeking to or
    retrieving the corresponding cursor.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        publish_time (google.protobuf.timestamp_pb2.Timestamp):
            Request the cursor of the first message with publish time
            greater than or equal to ``publish_time``. All messages
            thereafter are guaranteed to have publish times >=
            ``publish_time``.

            This field is a member of `oneof`_ ``time``.
        event_time (google.protobuf.timestamp_pb2.Timestamp):
            Request the cursor of the first message with event time
            greater than or equal to ``event_time``. If messages are
            missing an event time, the publish time is used as a
            fallback. As event times are user supplied, subsequent
            messages may have event times less than ``event_time`` and
            should be filtered by the client, if necessary.

            This field is a member of `oneof`_ ``time``.
    """

    publish_time = proto.Field(
        proto.MESSAGE, number=1, oneof="time", message=timestamp_pb2.Timestamp,
    )
    event_time = proto.Field(
        proto.MESSAGE, number=2, oneof="time", message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
