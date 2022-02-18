from django.core.management import BaseCommand

from apps.email_notifications.tasks import my_task
from apps.nova_poshta.api import update_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_data()
