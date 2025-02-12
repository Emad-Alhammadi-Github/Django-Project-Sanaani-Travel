from django.shortcuts import render, get_object_or_404, redirect
from ..models import Trip,City,TravelType,TripCategory,Vehicle
from django.db.models import Q
import os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Count
#####################################  ادارة الرحلات ##################################################################

@login_required(login_url='loginadmin')
def trip_list(request):
    query = request.GET.get('q', '')
    trips = Trip.objects.filter(Q(departure__name__icontains=query) | Q(destination__name__icontains=query))
    city = City.objects.all()  
    traveltype = TravelType.objects.all()  
    tripcategory = TripCategory.objects.all()  
    vehicle = Vehicle.objects.all()
    return render(request, 'dashboard/Trips.html', {'trips': trips, 'query': query,'city': city,'traveltype': traveltype,'tripcategory': tripcategory,'vehicle': vehicle})


def trip_filter(request):
    trips = Trip.objects.all()
    city = City.objects.all()  
    traveltype = TravelType.objects.all()  
    tripcategory = TripCategory.objects.all()  
    vehicle = Vehicle.objects.all()
    if request.method == 'POST':
        specific_date = request.POST.get('specific_date', None)
        
        if specific_date:
            try:
                specific_date = datetime.strptime(specific_date, "%Y-%m-%d").date()
                trips = trips.filter(date=specific_date)
            except ValueError:
                trips = trips
        if 'new_trips' in request.POST:
            trips = trips.filter(date__gte=datetime.today())
        if 'highest_price' in request.POST:
            trips = trips.order_by('-seat_price')
        if 'lowest_price' in request.POST:
            trips = trips.order_by('seat_price')
        if 'most_booked' in request.POST:
            trips = trips.annotate(booking_count=Count('passengers')).order_by('-booking_count')

    return render(request, 'dashboard/Trips.html', {'trips': trips,'city': city,'traveltype': traveltype,'tripcategory': tripcategory,'vehicle': vehicle})




@login_required(login_url='loginadmin')
def trip_detail(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    return render(request, 'dashboard/Trips_detail.html', {'trip': trip})



@login_required(login_url='loginadmin')
def add_trip(request):
    if request.method == 'POST':
        city_id_from= request.POST.get('departure') 
        city_id_to= request.POST.get('destination') 
        travel_type_id= request.POST.get('travel_type') 
        trip_category_id= request.POST.get('trip_category') 
        vehicle_type_id= request.POST.get('vehicle_type') 

        departure = get_object_or_404(City, id=city_id_from) 
        destination = get_object_or_404(City, id=city_id_to) 
        travel_type = get_object_or_404(TravelType, id=travel_type_id) 
        trip_category = get_object_or_404(TripCategory, id=trip_category_id) 
        vehicle_type = get_object_or_404(Vehicle, id=vehicle_type_id) 

        is_internal = departure.nationality == destination.nationality
        trip = Trip(
            departure=departure,
            destination=destination,
            travel_type=travel_type,
            trip_category=trip_category,
            vehicle_type=vehicle_type,
            date=request.POST['date'],
            time=request.POST['time'],
            seat_count=request.POST['seat_count'],
            seat_price=request.POST['seat_price'],
            details=request.POST['details'],
            image=request.FILES['image'],
            is_internal=is_internal
        )
        trip.save()
        return redirect('trip_list')
    return render(request, 'dashboard/Trips.html')


@login_required(login_url='loginadmin')
def edit_trip(request):
    if request.method == 'POST':
        trip_id = request.POST.get('id')
        trip = get_object_or_404(Trip, id=trip_id)
        city_id_from= request.POST.get('departure') 
        city_id_to= request.POST.get('destination') 
        travel_type_id= request.POST.get('travel_type') 
        trip_category_id= request.POST.get('trip_category') 
        vehicle_type_id= request.POST.get('vehicle_type') 

        departure = get_object_or_404(City, id=city_id_from) 
        destination = get_object_or_404(City, id=city_id_to) 
        travel_type = get_object_or_404(TravelType, id=travel_type_id) 
        trip_category = get_object_or_404(TripCategory, id=trip_category_id) 
        vehicle_type = get_object_or_404(Vehicle, id=vehicle_type_id) 

        trip.departure = departure
        trip.destination = destination
        trip.travel_type = travel_type
        trip.trip_category = trip_category
        trip.vehicle_type = vehicle_type
        trip.date = request.POST['date']
        trip.time = request.POST['time']
        trip.seat_count = request.POST['seat_count']
        trip.seat_price = request.POST['seat_price']
        trip.details = request.POST['details']
        
        if 'image' in request.FILES and request.FILES['image']:
            trip.image = request.FILES['image']
        
        trip.save() 
        return redirect('trip_list')



    return render(request, 'dashboard/Trips.html', {'trip': trip})


@login_required(login_url='loginadmin')
def delete_trip(request):
    if request.method == 'POST':
        trip_id = request.POST.get('id')
        trip = get_object_or_404(Trip, id=trip_id)

        if trip.image:
            if os.path.isfile(trip.image.path):
                os.remove(trip.image.path)
        trip.delete() 
        return redirect('trip_list') 
    return redirect('trip_list')


#####################################  ادارة الرحلات ##################################################################