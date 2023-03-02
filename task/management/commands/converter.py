from time import sleep

from django.conf import settings
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

                from_path = settings.DATA_DIR / task.path
                to_path =  settings.DATA_DIR / (task.path + '.mp3')

                failed = False
                message = ''
                try:
                    convert2mp3(from_path, to_path)
                except Exception as e:
                    failed = True
                    message = str(e)

                task.status = Task.Status.FINISHED
                task.finished_at = timezone.now()
                task.failed = failed
                task.message = message
                task.save()

            sleep(5)
