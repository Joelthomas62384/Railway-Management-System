# Generated by Django 4.2.6 on 2023-10-26 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trainstation', '0033_ticketbooking_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketbooking',
            name='discounted_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
