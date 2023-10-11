from django.db import models

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
    stops = models.ManyToManyField('Station', through='RouteStop')
    train = models.ForeignKey(Train,null=True,on_delete=models.SET_NULL)
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Routes"


class RouteStop(models.Model):
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    station = models.ForeignKey('Station', on_delete=models.CASCADE)
    Platform = models.PositiveIntegerField()
    arrival = models.TimeField(null=True,blank=True)
    Departure = models.TimeField(null=True,blank=True)

    
    
    class Meta:
        unique_together = ['route', 'station']
        ordering = ['Platform']
