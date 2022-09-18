from django.db import models
from django.core.files import File
from uuid import uuid4
import os


def get_audio_upload_path(filename, instance):
    filename = f'{uuid4()}.' + instance.split('.')[-1]
    return os.path.join("uploads/custom_audio/", filename)


def get_audio_voice_path(filename, instance):
    filename = f'{uuid4()}.' + instance.split('.')[-1]
    return os.path.join("voices/", filename)


def get_archive_path(filename, instance):
    filename = f'{uuid4()}.' + instance.split('.')[-1]
    return os.path.join("submissions/", filename)


class Audio(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    audio = models.FileField(upload_to=get_audio_upload_path)
    voice = models.IntegerField(default=225)
    is_processed = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='audio', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']


class Voice(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, default='Безымянный голос')
    url = models.FileField(upload_to=get_audio_voice_path)

    class Meta:
        ordering = ['name']


class Submission(models.Model):
    archive = models.FileField(upload_to=get_archive_path)
    name = models.CharField(max_length=50, default='Безымянный набор')
    owner = models.ForeignKey('auth.User', related_name='archive', on_delete=models.CASCADE)
