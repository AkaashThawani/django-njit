# Generated by Django 4.2.5 on 2023-12-05 02:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
