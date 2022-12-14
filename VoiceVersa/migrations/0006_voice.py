# Generated by Django 4.1 on 2022-09-18 12:24

import VoiceVersa.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VoiceVersa', '0005_alter_audio_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(upload_to=VoiceVersa.models.get_audio_voice_path)),
                ('number', models.IntegerField()),
            ],
            options={
                'ordering': ['number'],
            },
        ),
    ]
