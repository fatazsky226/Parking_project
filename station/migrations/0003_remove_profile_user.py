# Generated by Django 5.1.2 on 2024-10-15 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0002_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
    ]
