
from django.contrib import admin
from .models import *

class StationAdmin(admin.ModelAdmin):
    list_display = ( 'name','station_id', 'lattitue', 'longitude','platform')  # Include 'station_id' and other model fields




class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 1 

class RouteAdmin(admin.ModelAdmin):
    
    search_field = ('name')
    inlines = [RouteStopInline]
    


# Define the admin class for RouteStop
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ('route', 'station', 'Platform','arrival','Departure','Distance','reaching_time')
    list_filter = ('route', 'station')
    search_fields = ('route__name', 'station__name')


class TrainAdmin(admin.ModelAdmin):
    list_display = ("name","train_id","capacity","train_type","speed")

    

admin.site.register(RouteStop, RouteStopAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(Train,TrainAdmin)


