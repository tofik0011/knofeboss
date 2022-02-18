from django.core.management import BaseCommand

from apps.email_notifications.tasks import my_task


class Command(BaseCommand):
    def handle(self, *args, **options):
        my_task.delay('Хуй пизда')
