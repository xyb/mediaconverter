import os
from io import StringIO

from django.core.management import call_command
from django.test import override_settings
from django.urls import reverse

from pathlib import Path
from rest_framework import status
from rest_framework.test import APITestCase

from task.models import Task


TEST_ASSERTS_DIR = BASE_DIR = Path(__file__).resolve().parent / 'asserts'


class TaskTest(APITestCase):
    def test_create_convert_task(self):
        url = reverse('task-list')
        data = {'from_path': 'cat-meow.wav', 'to_path': 'cat-meow.mp3'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.get()
        self.assertEqual(task.to_path, 'cat-meow.mp3')
        self.assertEqual(task.status, Task.Status.INITED)

    @override_settings(DATA_DIR=TEST_ASSERTS_DIR)
    def test_converter(self):
        url = reverse('task-list')
        from_path = 'cat-meow.wav'
        to_path = 'cat-meow.mp3'
        data = {'from_path': from_path, 'to_path': to_path}
        self.client.post(url, data, format='json')
        if os.path.exists(to_path):
            os.unlink(to_path)

        self.call_command('--once')

        self.assertTrue(
            os.path.exists(Task.objects.get().get_full_to_path()),
        )

    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            "converter",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()
