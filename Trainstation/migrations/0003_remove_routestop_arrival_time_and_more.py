# Generated by Django 4.2.6 on 2023-10-09 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Trainstation', '0002_route_routestop_route_stops'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routestop',
            name='arrival_time',
        ),
        migrations.RemoveField(
            model_name='routestop',
            name='departure_time',
        ),
    ]
