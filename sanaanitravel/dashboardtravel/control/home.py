from django.shortcuts import render, get_object_or_404, redirect
from ..models import Trip,Contact, Passenger,City,TravelType,TripCategory,Employee,Nationality,ReservationRequest
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal
import os
from django.conf import settings
from ..forms import ContactForm 

#####################################   الرئيسية ##################################################################

#صفحة الرئيسية
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


#صفحة البحث الرحلة
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





#صفحة نجاح الحجز
def success_page(request):
    return render(request, 'home/success_page.html')

#صفحة خطأ الحجز
def error_checkOut(request):
    return render(request, 'home/error_checkOut.html')

# صفحة عن الموقع
def about_view(request):
    return render(request, 'home/about.html')

# صفحة اتصل بنا
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you') 
    else:
        form = ContactForm()
    
    return render(request, 'home/contact.html', {'form': form})

def thank_you_view(request):
    return render(request, 'home/thank_you.html')

def tripshome(request):
    trips = Trip.objects.all() 
    cities=City.objects.all()
    travel_types=TravelType.objects.all()
    trip_category=TripCategory.objects.all()
    print(f"Trips: {trips}")
    if not trips.exists():
        context = {"message": "لا توجد رحلات متاحة حاليًا."}
        return render(request, 'home/tripshome.html', {'context': context,'trips': trips,'cities':cities,'travel_types':travel_types,'trip_category':trip_category})
    else:
        return render(request, 'home/tripshome.html', {'trips': trips,'cities':cities,'travel_types':travel_types,'trip_category':trip_category})