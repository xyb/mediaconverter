from time import sleep
#import traceback

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from task.converter import convert2mp3
from task.models import Task
from task.path import safe_join


class Command(BaseCommand):
    help = 'run convert process'

    def handle(self, *args, **options):
        while True:
            tasks = Task.objects.filter(status=Task.Status.INITED)
            for task in tasks:
                print(f'start convert {task.from_path} to {task.to_path}')
                task.status = Task.Status.STARTED
                task.started_at = timezone.now()
                task.save()

                failed = False
                message = ''
                try:
                    from_path = safe_join(settings.DATA_DIR, task.from_path)
                    to_path =  safe_join(settings.DATA_DIR, task.to_path)
                    convert2mp3(from_path, to_path)
                    print(f'convert {task.to_path} successed.')
                except Exception as e:
                    print(f'convert {task.to_path} failed.')
                    failed = True
                    #tb = traceback.format_exc()
                    #message = f'{e}\n{tb}'
                    message = f'{e}'

                task.status = Task.Status.FINISHED
                task.finished_at = timezone.now()
                task.failed = failed
                task.message = message
                task.save()

            sleep(5)
