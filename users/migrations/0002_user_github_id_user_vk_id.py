# Generated by Django 4.2 on 2024-09-21 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='github_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='vk_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
