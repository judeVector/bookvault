from django.core.management.base import BaseCommand

from api.message_broker import consumer


class Command(BaseCommand):
    help = "Starts the RabbitMQ consumer"

    def handle(self, *args, **kwargs):
        consumer.consume_borrow_messages()
