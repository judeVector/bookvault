from django.core.management.base import BaseCommand

from api.helpers import consume_messages


class Command(BaseCommand):
    help = "Starts the RabbitMQ consumer"

    def handle(self, *args, **kwargs):
        consume_messages()
