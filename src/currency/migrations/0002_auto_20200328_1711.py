# Generated by Django 2.2.10 on 2020-03-28 17:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
