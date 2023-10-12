from django.db import models
from datetime import timedelta, datetime, time
from .utils import calculate_distance_and_time
from math import ceil


class Train(models.Model):
    TRAIN_TYPE_CHOICES = (
        ('express', 'Express Train'),
        ('shatabdi', 'Shatabdi Express'),
        ('rajdhani', 'Rajdhani Express'),
        ('duronto', 'Duronto Express'),
        ('jan_shatabdi', 'Jan Shatabdi Express'),
        ('garib_rath', 'Garib Rath Express'),
        ('superfast', 'Superfast Train'),
        ('passenger', 'Passenger Train'),
        ('local', 'Local Train'),
        ('mail_express', 'Mail/Express Train'),
        ('goods_freight', 'Goods/Freight Train'),
        ('special', 'Special Train'),
        ('other', 'Other'),
    )

    train_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    train_type = models.CharField(max_length=50, choices=TRAIN_TYPE_CHOICES)
    speed = models.DecimalField(max_digits=5, decimal_places=2)
    # Add more fields as needed, such as train schedule, status, etc.

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Trains"



class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default="",null=True)
    lattitue = models.CharField(max_length=100,default="",null=True)
    longitude = models.CharField(max_length=100,default="",null=True)
    platform = models.IntegerField(default=0,null=True)

    def __str__(self):
        return self.name  
    
    class Meta:
        verbose_name_plural = "Stations"


class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    start_time = models.TimeField(null=True)
    start_station = models.ForeignKey(Station,on_delete=models.CASCADE,related_name="start_station_routes",null=True,blank=True)
    stops = models.ManyToManyField('Station', through='RouteStop')
    train = models.ForeignKey(Train,null=True,on_delete=models.SET_NULL)
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Routes"
    def save(self, *args, **kwargs):
        super(Route, self).save(*args, **kwargs)

        # Check if there are no RouteStops associated with this Route
        if not self.routestop_set.exists():
            # Create the first RouteStop instance with the start station and start time
            start_datetime = datetime.combine(datetime.today(), self.start_time)

            # Creating a timedelta of 5 minutes
            time_delta = timedelta(minutes=5)

            # Adding timedelta to the datetime object
            new_datetime = start_datetime + time_delta

            # Extracting the time component from the new datetime object
            new_time = new_datetime.time()

            # Now, you can use new_time as your departure time in RouteStop
            first_route_stop = RouteStop(route=self, station=self.start_station, Platform=0, arrival=self.start_time, Departure=new_time)
            first_route_stop.save()



class RouteStop(models.Model):
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    station = models.ForeignKey('Station', on_delete=models.CASCADE)
    Platform = models.PositiveIntegerField(default=0)
    arrival = models.TimeField(null=True,blank=True)
    Departure = models.TimeField(null=True,blank=True)
    reaching_time = models.PositiveIntegerField(null=True,blank=True,default=0)
    Distance = models.IntegerField(null=True,blank=True,default=0 ,verbose_name="Distance (KM)")

    
    
    class Meta:
        unique_together = ['route', 'station']
        ordering = ['id']
    def save(self, *args, **kwargs):
        # Check if the arrival field is already set
        if not self.arrival:
            route_model = Route.objects.get(route_id=self.route.route_id)
            train_model = Train.objects.get(train_id=route_model.train.train_id)
            train_speed = train_model.speed

            try:
                previous_stop = RouteStop.objects.filter(route=route_model).order_by('-id')[0]
            except RouteStop.DoesNotExist:
                previous_stop = None

            if previous_stop:
                distance, predicted_time = calculate_distance_and_time(previous_stop.station, self.station, ceil(train_speed))
                departure_datetime = datetime.combine(datetime.today(), previous_stop.Departure)
                time_delta = timedelta(minutes=predicted_time)
                self.reaching_time=ceil(predicted_time)
                new_arrival_datetime = departure_datetime + time_delta
                self.arrival = new_arrival_datetime.time()
                self.Distance = distance
                time_delta2 = timedelta(minutes=5)
                new_departure_datetime = new_arrival_datetime + time_delta2
                new_departure_time = new_departure_datetime.time()
                self.Departure = new_departure_time

        super(RouteStop, self).save(*args, **kwargs)