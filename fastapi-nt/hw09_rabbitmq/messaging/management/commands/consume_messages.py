import time

from django.core.management.base import BaseCommand
from django.conf import settings

from messaging.rabbitmq import connection_parameters, declare_queue


class Command(BaseCommand):
    help = "Consume messages from RabbitMQ and print them to the console."

    def handle(self, *args, **options):
        import pika

        with pika.BlockingConnection(connection_parameters()) as connection:
            channel = connection.channel()
            declare_queue(channel)
            channel.basic_qos(prefetch_count=1)

            self.stdout.write(
                self.style.SUCCESS("Waiting for messages. Press Ctrl+C to stop.")
            )

            try:
                while True:
                    method_frame, _, body = channel.basic_get(
                        queue=settings.RABBITMQ_QUEUE_NAME,
                        auto_ack=False,
                    )
                    if method_frame is None:
                        time.sleep(1)
                        continue

                    text = body.decode("utf-8")
                    self.stdout.write(self.style.SUCCESS(f"Received: {text}"))
                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING("Consumer stopped."))
