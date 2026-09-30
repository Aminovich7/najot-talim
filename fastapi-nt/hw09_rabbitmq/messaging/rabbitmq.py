from __future__ import annotations

from dataclasses import dataclass

import pika
from django.conf import settings


@dataclass(frozen=True)
class RabbitMQMessage:
    body: str
    routing_key: str


def connection_parameters() -> pika.ConnectionParameters:
    return pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        virtual_host=settings.RABBITMQ_VHOST,
        credentials=pika.PlainCredentials(
            settings.RABBITMQ_USERNAME,
            settings.RABBITMQ_PASSWORD,
        ),
        heartbeat=30,
        blocked_connection_timeout=30,
    )


def declare_queue(channel: pika.adapters.blocking_connection.BlockingChannel) -> None:
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME, durable=True)


def publish_message(message: str) -> None:
    with pika.BlockingConnection(connection_parameters()) as connection:
        channel = connection.channel()
        declare_queue(channel)
        channel.basic_publish(
            exchange="",
            routing_key=settings.RABBITMQ_QUEUE_NAME,
            body=message.encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2),
        )


def consume_one_message() -> RabbitMQMessage | None:
    with pika.BlockingConnection(connection_parameters()) as connection:
        channel = connection.channel()
        declare_queue(channel)
        method_frame, _, body = channel.basic_get(
            queue=settings.RABBITMQ_QUEUE_NAME,
            auto_ack=False,
        )
        if method_frame is None:
            return None
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return RabbitMQMessage(
            body=body.decode("utf-8"),
            routing_key=method_frame.routing_key,
        )
