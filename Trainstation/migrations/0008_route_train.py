# Generated by Django 4.2.6 on 2023-10-09 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Trainstation', '0007_train'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='train',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Trainstation.train'),
        ),
    ]
