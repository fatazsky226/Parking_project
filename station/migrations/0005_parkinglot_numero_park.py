# Generated by Django 5.1.2 on 2024-10-16 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0004_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkinglot',
            name='numero_park',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
