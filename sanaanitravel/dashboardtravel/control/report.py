from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import Trip, Passenger,Nationality,Vehicle,City
from datetime import date
from django.db.models import Sum
from datetime import datetime
from django.db import models
from django.http import JsonResponse

#####################################  ادارة التقارير ##################################################################

# @login_required(login_url='login')
def report_view(request):
    selected_year = request.GET.get("year", datetime.now().year)
    selected_year = int(selected_year)

    selected_travel_type = request.GET.get("travel_type")
    selected_city = request.GET.get("city")

    trips_query = Trip.objects.filter(date__year=selected_year)

    if selected_travel_type:
        trips_query = trips_query.filter(trip_category__name__icontains=selected_travel_type)

    if selected_city:
        city = City.objects.get(id=selected_city)
        trips_query = trips_query.filter(departure=city) 

    internal_trips = trips_query.filter(trip_category__name__icontains="داخلية").count()
    external_trips = trips_query.filter(trip_category__name__icontains="خارجية").count()
    private_trips = trips_query.filter(trip_category__name="خاصة").count()
    truck_trips = trips_query.filter(trip_category__name="شاحنات").count()

    monthly_income = trips_query.aggregate(models.Sum("seat_price"))["seat_price__sum"] or 0
    mid_year_income = monthly_income * 6
    full_year_income = monthly_income * 12
    total_income = full_year_income
    # selected_year = request.GET.get("year", datetime.now().year)
    # selected_year = int(selected_year)


    # active_vehicles = Vehicle.objects.filter(status="in_service").count()
    # stopped_vehicles = Vehicle.objects.filter(status="out_of_service").count()
    total_vehicles = Vehicle.objects.count()
    active_vehicles = Trip.objects.values("vehicle_type__name").annotate(count=models.Count("vehicle_type")).count()
    stopped_vehicles=total_vehicles-active_vehicles

    
    most_used_vehicle = Trip.objects.values("vehicle_type__name").annotate(count=models.Count("vehicle_type")).order_by("-count").first()

    # internal_trips = Trip.objects.filter(trip_category__name__icontains="داخلية", date__year=selected_year).count()
    # external_trips = Trip.objects.filter(trip_category__name__icontains="خارجية", date__year=selected_year).count()
    # private_trips = Trip.objects.filter(trip_category__name="خاصة", date__year=selected_year).count()

    # monthly_income = Trip.objects.filter(date__year=selected_year).aggregate(models.Sum("seat_price"))["seat_price__sum"] or 0

    # mid_year_income = monthly_income * 6
    # full_year_income = monthly_income * 12
    # total_income = full_year_income




    


    nationalities = Nationality.objects.all()
    cities = City.objects.all()


    context = {
        "selected_year": selected_year,
        "monthly_income": monthly_income,
        "mid_year_income": mid_year_income,
        "full_year_income": full_year_income,
        "total_income": total_income,
        "internal_trips": internal_trips,
        "external_trips": external_trips,
        "private_trips": private_trips,
        "truck_trips": truck_trips,
        "active_vehicles": active_vehicles,
        "stopped_vehicles": stopped_vehicles,
        "total_vehicles": total_vehicles,
        "most_used_vehicle": most_used_vehicle["vehicle_type__name"] if most_used_vehicle else "N/A",
        "nationalities": nationalities,
        "cities": cities,
    }

    return render(request, 'dashboard/Reports.html', context)


def get_cities(request):
    nationality_id = request.GET.get('nationality_id')
    cities = City.objects.filter(nationality_id=nationality_id).values('id', 'name')
    return JsonResponse({'cities': list(cities)})
#####################################  ادارة التقارير ##################################################################