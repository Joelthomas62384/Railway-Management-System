from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from . models import *
from django.db.models import Q



def livetrain(request):
    return render(request,"livetrain.html")

def get_train(request):
    payload = []
    search = request.GET.get('term')

    train = Train.objects.all()

    try:
        search_int = int(search)

        train = train.filter(Q(train_id=search_int))
        if train:
            for i in train:
                payload.append(f"{i.train_id} ({i.name})")

    except ValueError:
        train = Train.objects.filter(Q(name__icontains=search))

        if train:
            for i in train:
                payload.append(f"{i.name} ({i.train_id})")
    return JsonResponse(payload, safe=False)


def showtrain(request):
    routes = []
    if request.method == "GET":
        train = request.GET.get("train")
        train_split = train.split("(")[0].strip()
        train = Train.objects.all()
        if train_split.isdigit():
            train = train.filter(train_id = train_split)
        else:
            train = train.filter(name=train_split)



        for i in train:
            route = Route.objects.filter(train=i)
            routes.append(route)
        
        
        context = {
            "route":routes
        }
    return render(request,"trainshow.html",context)


def live_status(request,id):
    routes = Route.objects.get(route_id=id)
    route_stops = RouteStop.objects.filter(route=routes)
    context = {
        'route_stops':route_stops
    }
    return render(request,"live-status.html",context)