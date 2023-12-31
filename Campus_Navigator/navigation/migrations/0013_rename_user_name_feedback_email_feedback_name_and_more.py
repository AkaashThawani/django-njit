# Generated by Django 4.2.5 on 2023-12-06 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0012_alter_searchlocation_search_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='user_name',
            new_name='email',
        ),
        migrations.AddField(
            model_name='feedback',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='comment',
            field=models.TextField(max_length=1000),
        ),
    ]
