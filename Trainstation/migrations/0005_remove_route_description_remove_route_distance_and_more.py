# Generated by Django 4.2.6 on 2023-10-09 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Trainstation', '0004_alter_routestop_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='description',
        ),
        migrations.RemoveField(
            model_name='route',
            name='distance',
        ),
        migrations.RemoveField(
            model_name='route',
            name='duration',
        ),
    ]