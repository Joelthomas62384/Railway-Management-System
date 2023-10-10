# Generated by Django 4.2.6 on 2023-10-09 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trainstation', '0006_route_start_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('train_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.PositiveIntegerField()),
                ('train_type', models.CharField(choices=[('express', 'Express Train'), ('shatabdi', 'Shatabdi Express'), ('rajdhani', 'Rajdhani Express'), ('duronto', 'Duronto Express'), ('jan_shatabdi', 'Jan Shatabdi Express'), ('garib_rath', 'Garib Rath Express'), ('superfast', 'Superfast Train'), ('passenger', 'Passenger Train'), ('local', 'Local Train'), ('mail_express', 'Mail/Express Train'), ('goods_freight', 'Goods/Freight Train'), ('special', 'Special Train'), ('other', 'Other')], max_length=50)),
                ('speed', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name_plural': 'Trains',
            },
        ),
    ]
