from django.db import models



class Task(models.Model):

    class Status(models.IntegerChoices):
        INITED = 1
        STARTED = 2
        FINISHED = 3

    path = models.CharField(max_length=1024)
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(blank=True)
    finished_at = models.DateTimeField(blank=True)
    failed = models.BooleanField(null=True)
    message = models.CharField(max_length=1000)
