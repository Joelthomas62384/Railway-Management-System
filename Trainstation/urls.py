from django.urls import path
from . import views
from . import liveviews

urlpatterns = [
    path("",views.home,name="home"),
    path("booking",views.booking,name="booking"),
    path("booking_form",views.booking_submit,name="bookingform"),
    path('station_names/', views.get_station, name='station_names'),
    path('search_trains', views.search_trains, name='search_trains'),
    path("ticketbooking",views.ticketboking,name="ticketbooking"),
    path('success/',views.success,name="success"),

# -------------------------------------------------------------------------------------------------
                                        # live tracking urls




    path("livetrain",liveviews.livetrain,name="livetrain"),
    path("get_train/",liveviews.get_train,name="getTrain"),
    path("showtrain",liveviews.showtrain,name="showtrain"),
    path("live-status/<int:id>",liveviews.live_status,name="livestatus")
    
]
