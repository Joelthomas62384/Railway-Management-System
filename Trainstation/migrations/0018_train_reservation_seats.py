# Generated by Django 4.2.6 on 2023-10-17 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trainstation', '0017_alter_routestop_reaching_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='reservation_seats',
            field=models.PositiveIntegerField(default=10),
        ),
    ]