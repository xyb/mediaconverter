from time import sleep

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from task.models import Task
from task.converter import convert2mp3


class Command(BaseCommand):
    help = 'run convert process'

    def handle(self, *args, **options):
        while True:
            tasks = Task.objects.filter(status=Task.Status.INITED)
            for task in tasks:
                task.status = Task.Status.STARTED
                task.started_at = timezone.now()
                task.save()

                failed = False
                message = ''
                try:
                    convert2mp3(task.path, task.path + '.mp3')
                except Exception as e:
                    failed = True
                    message = str(e)

                task.status = Task.Status.FINISHED
                task.finished_at = timezone.now()
                task.failed = failed
                task.message = message
                task.save()

            sleep(5)
