from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import Trip, Passenger,Nationality,Vehicle,City,ReservationRequest
from datetime import date
from datetime import datetime
from django.db import models
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.contrib import messages
#####################################  ادارة التقارير ##################################################################

# @login_required(login_url='login')

def calculate_income(trips_query):

    monthly_income = trips_query.aggregate(total_income=Sum("seat_price"))["total_income"] or 0
    mid_year_income = monthly_income * 6
    full_year_income = monthly_income * 12
    return monthly_income, mid_year_income, full_year_income

def filter_passengers(passengers, filters):

    return passengers.filter(**filters)

def report_view(request):
    trips = Trip.objects.all()
    passengers = Passenger.objects.all()

    selected_date = request.GET.get("year")
    current_year = datetime.now().year  

    if selected_date:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
        selected_year = selected_date.year  
        selected_month = selected_date.month  
        trips_query = trips.filter(date_added__year=selected_year, date_added__month=selected_month)  
    else:
        selected_date = None
        selected_year = current_year  
        selected_month = datetime.now().month  
        trips_query = trips.filter(date_added__year=selected_year, date_added__month=selected_month) 

    monthly_income, mid_year_income, full_year_income = calculate_income(trips_query)
    total_income = full_year_income

    # if selected_year == current_year:
        
    #     monthly_income, mid_year_income, full_year_income = calculate_income(trips_query)
    # else:
    #     monthly_income, mid_year_income, full_year_income = 0, 0, 0


    print(f"عدد الرحلات : {trips_query.count()}")

    total_income_check = trips_query.aggregate(total_income=Sum("seat_price"))["total_income"]
    print(f"إجمالي الدخل: {total_income_check}")


    internal_passengers = filter_passengers(passengers, {
        "trip_location__departure__nationality__name": "اليمن",
        "trip_location__destination__nationality__name": "اليمن",
        "trip_location__date_added__date" if selected_date else "trip_location__date_added__year": selected_date if selected_date else selected_year
    })
    is_yemeni_trip = internal_passengers.aggregate(total_paid=Sum("paid_amount"))["total_paid"] or 0

    external_passengers = passengers.exclude(
        trip_location__departure__nationality__name="اليمن",
        trip_location__destination__nationality__name="اليمن"
    ).filter(**{
        "trip_location__date_added__date" if selected_date else "trip_location__date_added__year": selected_date if selected_date else selected_year
    })
    is_no_yemeni_trip = external_passengers.aggregate(total_paid=Sum("paid_amount"))["total_paid"] or 0

    private_passengers = filter_passengers(passengers, {
        "trip_location__trip_category__name__icontains": "خاصة",
        "trip_location__date_added__date" if selected_date else "trip_location__date_added__year": selected_date if selected_date else selected_year
    })
    is_private_trip = private_passengers.aggregate(total_paid=Sum("paid_amount"))["total_paid"] or 0

    truck_passengers = filter_passengers(passengers, {
        "trip_location__trip_category__name__icontains": "عامة",
        "trip_location__date_added__date" if selected_date else "trip_location__date_added__year": selected_date if selected_date else selected_year
    })
    is_truck_trip = truck_passengers.aggregate(total_paid=Sum("paid_amount"))["total_paid"] or 0

    internal_trips = trips_query.filter(is_internal=True).count()
    external_trips = trips_query.filter(is_internal=False).count()
    private_trips = trips_query.filter(trip_category__name__icontains="خاصة").count()
    truck_trips = trips_query.filter(trip_category__name__icontains="عامة").count()

    total_passengers_internal = internal_passengers.count()
    total_passengers_external = external_passengers.count()
    total_passengers_private = private_passengers.count()
    total_passengers_public = truck_passengers.count()

    total_vehicles = Vehicle.objects.count()
    active_vehicles = trips_query.values("vehicle_type__name").annotate(count=Count("vehicle_type")).count()
    stopped_vehicles = total_vehicles - active_vehicles

    most_used_vehicle = trips_query.values("vehicle_type__name").annotate(count=Count("vehicle_type")).order_by("-count").first()

    vehicles_internal = Vehicle.objects.filter(
        trip__is_internal=True,
        **{"trip__date_added__date" if selected_date else "trip__date_added__year": selected_date if selected_date else selected_year}
    ).distinct().count()
    vehicles_external = Vehicle.objects.filter(
        trip__is_internal=False,
        **{"trip__date_added__date" if selected_date else "trip__date_added__year": selected_date if selected_date else selected_year}
    ).distinct().count()

    accepted_reservations = ReservationRequest.objects.filter(
        status="approved",
        **{"passenger__trip_location__date_added__date" if selected_date else "passenger__trip_location__date_added__year": selected_date if selected_date else selected_year}
    ).count()
    rejected_reservations = ReservationRequest.objects.filter(
        status="rejected",
        **{"passenger__trip_location__date_added__date" if selected_date else "passenger__trip_location__date_added__year": selected_date if selected_date else selected_year}
    ).count()

    nationality_report = []
    if selected_date:
        for nationality in Nationality.objects.filter(cities__departures__date_added__date=selected_date).distinct():
            nationality_trips = trips_query.filter(departure__nationality=nationality)
            nationality_passengers = Passenger.objects.filter(trip_location__in=nationality_trips).count()
            nationality_report.append({
                'name': nationality.name,
                'trips': nationality_trips.count(),
                'passengers': nationality_passengers,
            })
    else:
        for nationality in Nationality.objects.all():
            nationality_trips = trips.filter(departure__nationality=nationality)
            nationality_passengers = Passenger.objects.filter(trip_location__in=nationality_trips).count()
            nationality_report.append({
                'name': nationality.name,
                'trips': nationality_trips.count(),
                'passengers': nationality_passengers,
            })

    city_report = []
    if selected_date:
        for city in City.objects.filter(departures__date_added__date=selected_date).distinct():
            trip_count = trips_query.filter(departure=city).count()
            passenger_count = Passenger.objects.filter(trip_location__departure=city).count()
            city_report.append({
                'city_name': city.name,
                'trip_count': trip_count,
                'passenger_count': passenger_count,
            })
    else:
        for city in City.objects.all():
            trip_count = trips.filter(departure=city).count()
            passenger_count = Passenger.objects.filter(trip_location__departure=city).count()
            city_report.append({
                'city_name': city.name,
                'trip_count': trip_count,
                'passenger_count': passenger_count,
            })

    context = {
        "is_yemeni_trip": is_yemeni_trip,
        "is_no_yemeni_trip": is_no_yemeni_trip,
        "is_private_trip": is_private_trip,
        "is_truck_trip": is_truck_trip,
        "selected_date": selected_date,
        "selected_year": selected_year, 
        "monthly_income": monthly_income,
        "mid_year_income": mid_year_income,
        "full_year_income": full_year_income,
        "total_income": total_income,
        "internal_trips": internal_trips,
        "external_trips": external_trips,
        "private_trips": private_trips,
        "truck_trips": truck_trips,
        'vehicles_internal': vehicles_internal,
        'vehicles_external': vehicles_external,
        'total_passengers_internal': total_passengers_internal,
        'total_passengers_external': total_passengers_external,
        'total_passengers_private': total_passengers_private,
        'total_passengers_public': total_passengers_public,
        'accepted_reservations': accepted_reservations,
        'rejected_reservations': rejected_reservations,
        "active_vehicles": active_vehicles,
        "stopped_vehicles": stopped_vehicles,
        "total_vehicles": total_vehicles,
        'nationality_report': nationality_report,
        'city_report': city_report,
        "most_used_vehicle": most_used_vehicle["vehicle_type__name"] if most_used_vehicle else "N/A",
        "nationalities": Nationality.objects.all(),
        "cities": City.objects.all(),
    }

    return render(request, 'dashboard/Reports.html', context)


def get_cities(request):
    nationality_id = request.GET.get('nationality_id')
    cities = City.objects.filter(nationality_id=nationality_id).values('id', 'name')
    return JsonResponse({'cities': list(cities)})
#####################################  ادارة التقارير ##################################################################


