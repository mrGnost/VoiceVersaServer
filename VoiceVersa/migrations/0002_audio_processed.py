# Generated by Django 4.1 on 2022-09-13 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VoiceVersa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='processed',
            field=models.FileField(blank=True, upload_to='uploads/output_audio/'),
        ),
    ]
