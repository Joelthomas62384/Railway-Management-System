
from django.contrib import admin
from .models import *

class StationAdmin(admin.ModelAdmin):
    list_display = ('station_id', 'name', 'lattitue', 'longitude','platform')  # Include 'station_id' and other model fields




class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 1 

class RouteAdmin(admin.ModelAdmin):
    
    search_field = ('name')
    inlines = [RouteStopInline]
    


# Define the admin class for RouteStop
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ('route', 'station', 'Platform')
    list_filter = ('route', 'station')
    search_fields = ('route__name', 'station__name')


class TrainAdmin(admin.ModelAdmin):
    list_display = ("train_id","name","capacity","train_type","speed")

    

admin.site.register(RouteStop, RouteStopAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(Train,TrainAdmin)


