from datetime import datetime, time
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from .utils import calculate_distance_and_time,calculate_ticket_price,create_image_from_model
from math import ceil
from django.conf import settings
import razorpay




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
             
                from_stop = RouteStop.objects.filter(route=route, station=from_station).first()
                to_stop = RouteStop.objects.filter(route=route, station=to_station).first()
                
                if from_stop and to_stop and from_stop.id < to_stop.id:
                    correct_routes.append(route)
                    from_arrival.append(from_stop.arrival.strftime('%H:%M'))
                    to_arrival.append(to_stop.arrival.strftime('%H:%M'))
                   

        except Station.DoesNotExist:
            print(f"Station not found: {from_station_name} or {to_station_name}")
        except Route.DoesNotExist:
            print("No valid route found.")


        route_data = list(zip(correct_routes, from_arrival, to_arrival))

        route_data.sort(key=lambda x: datetime.strptime(x[1], '%H:%M'))


        sorted_routes = [item[0] for item in route_data]

        context = {
            "from_name": from_station_name,
            'to_name': to_station_name,
            'date': date,
            'train_with_arrival': set(route_data), 
            'empty': True if len(sorted_routes) < 1 else False
        }

        return render(request, "book_ticket.html", context)
    return render(request, "book_ticket.html")






def ticketboking(request):
 
    if request.method == "POST":
        from_station_name = request.POST.get("from")
        to_station_name = request.POST.get("to")
        email = request.POST.get("email")
        name = request.POST.get("name")
        date = request.POST.get("date")
        route = request.POST.get("route")
        reservation = request.POST.get("reservation")
        print(from_station_name, to_station_name, date, route, email, name, reservation)

        from_station = Station.objects.get(name=from_station_name)
        to_station = Station.objects.get(name=to_station_name)
        route = Route.objects.get(route_id=route)
        train_speed = route.train.speed
        basefair = route.train.base_fair
        additional_charges = route.train.additional_charge

        distance, _ = calculate_distance_and_time(from_station, to_station, ceil(train_speed))
        reservations = TicketBooking.objects.filter(reservation=True,event_date=date)
        total_price = calculate_ticket_price(base_fare=basefair, distance=distance, additional_charges=additional_charges, seat_reservation_fee=100 if len(reservations)<route.train.reservation_seats and eval(reservation) else 0)
        client = razorpay.Client(auth=(settings.KEY_ID,settings.KEY_SECRET))
        payment = client.order.create({'amount':ceil(total_price*100),'currency':"INR","payment_capture":1})
        print(total_price)

        existing_booking = TicketBooking.objects.filter(name=name, email=email, event_date=date).first()
        reservate = False
        seat_reservate = 0
        if len(reservations)<route.train.reservation_seats and eval(reservation):
            reservate = True
            seat_reservate = len(reservations)+1

        else:
            reservate = False
        
        if existing_booking:
            id = existing_booking.id
            existing_booking.razor_pay_order_id = payment['id']
            existing_booking.save()            
        else:
            Trainbook = TicketBooking(name=name, route=route, email=email, from_station=from_station, to_station=to_station, event_date=date,reservation=reservate, reservation_seat=seat_reservate, total_price=ceil(total_price))
            Trainbook.save()
            id = Trainbook.id
            Trainbook.razor_pay_order_id = payment['id']
            Trainbook.save()
        print(payment)
        print("reservation count : ",len(reservations))
        context = {"Amount": ceil(total_price), "id": id,"payment":payment}
        return render(request, "payment.html", context)

    return redirect("home")


def success(request):
    order_id = request.GET.get("razorpay_order_id")
    tickets = TicketBooking.objects.get(razor_pay_order_id=order_id)
    tickets.paid=True
    tickets.save()
    create_image_from_model(tickets) 
    context = {
        "image":tickets.ticket_image
    }
    return render(request,"show_ticket.html",context)
