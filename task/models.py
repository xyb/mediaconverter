from django.conf import settings
from django.db import models

from task.path import safe_join


class Task(models.Model):
    class Status(models.TextChoices):
        INITED = "Inited"
        STARTED = "Started"
        FINISHED = "Finished"

    from_path = models.CharField(max_length=1024)
    to_path = models.CharField(max_length=1024)
    status = models.CharField(
        max_length=30,
        editable=False,
        choices=Status.choices,
        default=Status.INITED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(blank=True, null=True, editable=False)
    finished_at = models.DateTimeField(blank=True, null=True, editable=False)
    failed = models.BooleanField(default=False, editable=False)
    message = models.CharField(max_length=1000, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=["to_path"]),
        ]

    def get_full_from_path(self):
        return safe_join(settings.DATA_DIR, self.from_path)

    def get_full_to_path(self):
        return safe_join(settings.DATA_DIR, self.to_path)
