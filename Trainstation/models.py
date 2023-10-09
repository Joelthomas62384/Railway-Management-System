from django.db import models

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
    description = models.TextField()
    stops = models.ManyToManyField('Station', through='RouteStop')
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Routes"


class RouteStop(models.Model):
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    station = models.ForeignKey('Station', on_delete=models.CASCADE)
    stop_order = models.PositiveIntegerField()
    arrival_time = models.TimeField()
    departure_time = models.TimeField()

    class Meta:
        unique_together = ['route', 'station']
        ordering = ['stop_order']
