# Generated by Django 4.2.6 on 2023-10-09 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('station_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100, null=True)),
                ('lattitue', models.CharField(default='', max_length=100, null=True)),
                ('longitude', models.CharField(default='', max_length=100, null=True)),
                ('platform', models.IntegerField(default=0, null=True)),
            ],
            options={
                'verbose_name_plural': 'Stations',
            },
        ),
    ]