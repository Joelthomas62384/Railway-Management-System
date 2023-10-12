from django.shortcuts import render,HttpResponse

# Create your views here.

def home(request):
    return render(request,"index.html")

def booking(request):
    return render(request,"booking.html")
