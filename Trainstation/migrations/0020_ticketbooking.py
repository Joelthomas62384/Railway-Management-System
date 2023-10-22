# Generated by Django 4.2.6 on 2023-10-18 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Trainstation', '0019_alter_train_reservation_seats'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('event_date', models.DateField()),
                ('num_tickets', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('from_station', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Departures', to='Trainstation.station')),
                ('to_station', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Arrivals', to='Trainstation.station')),
            ],
        ),
    ]