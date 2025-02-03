from django.shortcuts import render, get_object_or_404, redirect
from ..models import Trip, Passenger,City,TravelType,TripCategory,Employee,Nationality,ReservationRequest
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal
import os
from django.conf import settings


#####################################   الرئيسية ##################################################################

def home(request):
    trips = Trip.objects.all() 
    cities=City.objects.all()
    travel_types=TravelType.objects.all()
    trip_category=TripCategory.objects.all()
    print(f"Trips: {trips}")
    if not trips.exists():
        context = {"message": "لا توجد رحلات متاحة حاليًا."}
        return render(request, 'home/home.html', {'context': context,'trips': trips,'cities':cities,'travel_types':travel_types,'trip_category':trip_category})
    else:
        return render(request, 'home/home.html', {'trips': trips,'cities':cities,'travel_types':travel_types,'trip_category':trip_category})




# def home(request):
#     trips = Trip.objects.all() 
#     cities=City.objects.all()
#     travel_types=TravelType.objects.all()
#     trip_category=TripCategory.objects.all()
#     print(f"Trips: {trips}")
#     if not trips.exists():
#         context = {"message": "لا توجد رحلات متاحة حاليًا."}
#     else:
#         context = {"trips": trips}
#     # context = {
#     # 'trips': trips,
#     # 'cities': cities,
#     # 'travel_types': travel_types,
#     # 'trip_category': trip_category
#     # }
#     return render(request, 'home/home.html', {'context': context,'cities':cities,'travel_types':travel_types,'trip_category':trip_category})

def search_trips(request):
    departure_city = request.POST.get('departure_city')
    destination_city = request.POST.get('destination_city')
    trip_date = request.POST.get('trip_date')
    travel_type = request.POST.get('travel_type')

    trips = Trip.objects.all()

    if departure_city:
        trips = trips.filter(departure_id=departure_city)
    if destination_city:
        trips = trips.filter(destination_id=destination_city)
    if trip_date:
        trips = trips.filter(date=trip_date)
    if travel_type:
        trips = trips.filter(travel_type_id=travel_type)

    context = {
        'trips': trips,
        'cities': City.objects.all(),
        'travel_types': TravelType.objects.all(),
        'trip_category': TripCategory.objects.all() 
    }
    return render(request, 'home/home.html', context)






def success_page(request):
    return render(request, 'home/success_page.html')

def error_checkOut(request):
    return render(request, 'home/error_checkOut.html')