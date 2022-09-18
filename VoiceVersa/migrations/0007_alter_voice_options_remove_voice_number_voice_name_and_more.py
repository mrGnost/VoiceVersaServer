# Generated by Django 4.1 on 2022-09-18 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VoiceVersa', '0006_voice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='voice',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='voice',
            name='number',
        ),
        migrations.AddField(
            model_name='voice',
            name='name',
            field=models.CharField(default='Безымянный голос', max_length=50),
        ),
        migrations.AlterField(
            model_name='voice',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
