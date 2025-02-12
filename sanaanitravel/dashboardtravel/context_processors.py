from .models import Vehicle, Driver, Passenger,Trip,ReservationRequest
from django.db.models import Sum
from datetime import date
from django.http import JsonResponse
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import models
# @login_required

def dashboard_data(request):
    today = date.today()
    todayrr = timezone.now().date()

    today_income = Passenger.objects.filter(date_added__date=todayrr).aggregate(total_income=Sum('paid_amount'))['total_income'] or 0
    current_year = date.today().year
    year_income = Passenger.objects.filter(date_added__year=current_year).aggregate(total_income=Sum('paid_amount'))['total_income'] or 0



    total_vehicles = Vehicle.objects.count()
    in_service = Trip.objects.values("vehicle_type__name").annotate(count=models.Count("vehicle_type")).count()
    out_of_service=total_vehicles-in_service


    total_drivers = Driver.objects.count()
    in_drivers = Vehicle.objects.values("driver__name").annotate(count=models.Count("name")).count()
    out_of_drivers=total_drivers - in_drivers

    yearly_passenger = ReservationRequest.objects.filter(request_date__year=current_year).count()
# 
    daily_passenger = ReservationRequest.objects.filter(request_date=today).count()

    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    weekly_passengers = ReservationRequest.objects.filter(request_date__range=[start_of_week, end_of_week]).count()


    return {
        'today_income': today_income,
        'year_income': year_income,
        'total_vehicles': total_vehicles,
        'in_service': in_service,
        'out_of_service': out_of_service,
        'total_drivers': total_drivers,
        'in_drivers': in_drivers,
        'out_of_drivers': out_of_drivers,
        'yearly_passenger': yearly_passenger,
        'weekly_passengers': weekly_passengers,
        'daily_passenger': daily_passenger,
    }
