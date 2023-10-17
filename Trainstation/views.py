from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.core import serializers
from django.http import JsonResponse
from .models import *

# Create your views here.

def home(request):
    return render(request,"index.html")


def get_station(request):
    search = request.GET.get('term')
    if search:
        result = Station.objects.filter(name__startswith=search)
        mylist = []
        mylist+=[i.name for i in result]
        return JsonResponse(mylist,safe=False)
    
    # return JsonResponse(payload,safe=False)





def booking (request):
    return render(request,"train_search.html")


def booking_submit(request):
    if request.method == "POST":
        from_station = request.POST.get('from')
        to_station = request.POST.get('to')
        date = request.POST.get('date')
        number = request.POST.get('seats')

        print(from_station,to_station,date,number)
    return redirect("booking")




def search_trains(request):
    if request.method == "POST":
        from_station_name = request.POST.get("from")
        to_station_name = request.POST.get("to")
        try:
            from_station = Station.objects.get(name=from_station_name)
            to_station = Station.objects.get(name=to_station_name)
          

            routes = Route.objects.filter(
                        routestop__station=from_station
                    ).filter(
                        routestop__station=to_station
                    )

            correct_routes = []
            for route in routes:
                # Check if the 'from' station comes before the 'to' station in this route
                from_stop = RouteStop.objects.filter(route=route, station=from_station).first()
                to_stop = RouteStop.objects.filter(route=route, station=to_station).first()
                
                if from_stop and to_stop and from_stop.id < to_stop.id:
                    correct_routes.append(route)


        except Station.DoesNotExist:
            print(f"Station not found: {from_station_name} or {to_station_name}")
        except Route.DoesNotExist:
            print("No valid route found.")
        print(from_station_name,to_station_name)
        print(routes)
        print(correct_routes)

        context = {
            "from_name":from_station_name,
            'to_name':to_station_name
        }

    return render(request, "book_ticket.html",context)



