from .models import Task
from rest_framework import serializers


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'path', 'status', 'created_at', 'started_at',
                  'finished_at', 'failed', 'message']
