from time import sleep

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from task.models import Task


class Command(BaseCommand):
    help = 'run convert process'

    def handle(self, *args, **options):
        while True:
            tasks = Task.objects.filter(status=Task.Status.INITED)
            for task in tasks:
                task.status = Task.Status.STARTED
                task.started_at = timezone.now()
                task.save()
                print(task.path)
                # TODO: convert
                task.status = Task.Status.FINISHED
                task.save()

            sleep(5)
