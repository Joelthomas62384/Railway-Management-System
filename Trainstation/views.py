from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.core import serializers
from django.http import JsonResponse
from .models import *
from .utils import calculate_distance_and_time

# Create your views here.

def home(request):
    return render(request,"index.html")


def get_station(request):
    search = request.GET.get('term')
    mylist = []
    if search:
        result = Station.objects.filter(name__startswith=search)
        mylist+=[i.name for i in result]
    return JsonResponse(mylist,safe=False)
    






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
    correct_routes = []
    from_arrival = []
    to_arrival = []
    if request.method == "POST":
        from_station_name = request.POST.get("from")
        to_station_name = request.POST.get("to")
        date = request.POST.get("date")
        
        try:
            from_station = Station.objects.get(name=from_station_name)
            to_station = Station.objects.get(name=to_station_name)
          

            routes = Route.objects.filter(
                        routestop__station=from_station
                    ).filter(
                        routestop__station=to_station
                    )

            

            for route in routes:
                # Check if the 'from' station comes before the 'to' station in this route
                from_stop = RouteStop.objects.filter(route=route, station=from_station).first()
                to_stop = RouteStop.objects.filter(route=route, station=to_station).first()
                
                if from_stop and to_stop and from_stop.id < to_stop.id:
                    correct_routes.append(route)
                    from_arrival.append(from_stop.arrival)
                    to_arrival.append(to_stop.arrival)
                   


        except Station.DoesNotExist:
            print(f"Station not found: {from_station_name} or {to_station_name}")
        except Route.DoesNotExist:
            print("No valid route found.")
        route_data = list(zip(correct_routes, from_arrival, to_arrival))

        # Sort the list based on the arrival times (from_arrival and to_arrival)
        route_data.sort(key=lambda x: (x[1], x[2]))

        # Extract the sorted routes from the sorted list
        sorted_routes = [item[0] for item in route_data]
        sorted_arrival = [item[1] for item in route_data]
        sorted_to = [item[2] for item in route_data]
        
        context = {
            "from_name":from_station_name,
            'to_name':to_station_name,
            'date':date,
            'train_with_arrival':zip(sorted_routes,sorted_arrival,sorted_to),
            'empty': True if len(sorted_routes)<1 else False
        }

        return render(request, "book_ticket.html",context)
    return render(request, "book_ticket.html")





def ticketboking(request):
    if request.method == "POST":
        from_station_name = request.POST.get("from")
        to_station_name = request.POST.get("to")
        email = request.POST.get("email")
        name = request.POST.get("name")
        date = request.POST.get("date")
        rotue = request.POST.get("route")
        print(from_station_name,to_station_name,date,rotue,email,name)

    return redirect("search_trains")
