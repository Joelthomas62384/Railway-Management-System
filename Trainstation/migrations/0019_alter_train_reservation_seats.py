# Generated by Django 4.2.6 on 2023-10-17 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trainstation', '0018_train_reservation_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='train',
            name='reservation_seats',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
