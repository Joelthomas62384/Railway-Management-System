# Generated by Django 4.2.6 on 2023-10-12 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trainstation', '0015_remove_routestop_reached_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='routestop',
            name='reaching_time',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]