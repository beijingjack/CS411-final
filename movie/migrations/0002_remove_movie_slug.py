# Generated by Django 2.1.2 on 2018-10-31 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='slug',
        ),
    ]
