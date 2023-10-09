
from django.contrib import admin
from .models import Station

class StationAdmin(admin.ModelAdmin):
    list_display = ('station_id', 'name', 'lattitue', 'longitude','platform')  # Include 'station_id' and other model fields



class RouteAdmin(admin.ModelAdmin):
    list_display = ("route_id","name","description","stops","distance","duration")
# Register the Station model with the custom admin class
admin.site.register(Station, StationAdmin)


