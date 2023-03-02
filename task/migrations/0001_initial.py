# Generated by Django 4.1.7 on 2023-03-02 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_path', models.CharField(max_length=1024)),
                ('to_path', models.CharField(max_length=1024)),
                ('status', models.CharField(choices=[('Inited', 'Inited'), ('Started', 'Started'), ('Finished', 'Finished')], default='Inited', editable=False, max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('started_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('finished_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('failed', models.BooleanField(default=False, editable=False)),
                ('message', models.CharField(editable=False, max_length=1000)),
            ],
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['to_path'], name='task_task_to_path_9320fe_idx'),
        ),
    ]
