from django.shortcuts import render, get_object_or_404, redirect
from ..models import Trip, Passenger,Employee,Service,Driver,Vehicle,ReservationRequest
from django.db.models import Q
import os
from django.db.models import Sum
from datetime import date
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required

##################################### الصفحة الرئيسية ##################################################################




def home_dashboard(request):
    today = date.today()
    today_income = Passenger.objects.filter(trip_date=today).aggregate(total_income=Sum('paid_amount'))['total_income'] or 0
    print(f"Income for today: {today_income}")
    current_year = date.today().year
    year_income = Passenger.objects.filter(trip_date__year=current_year).aggregate(total_income=Sum('paid_amount'))['total_income'] or 0
    print(f"Income for the year: {year_income}") 
    



    # today = date.today()
    # current_year = today.year

    # daily_profit = Trip.objects.filter(date=today).aggregate(total=Sum('seat_price'))['total'] or 0
    # yearly_profit = Trip.objects.filter(date__year=current_year).aggregate(total=Sum('seat_price'))['total'] or 0


    # total_vehicles = Vehicle.objects.count()
    # in_service = Trip.objects.count()
    # out_of_service=total_vehicles - in_service


    # total_drivers = Driver.objects.count()
    # in_drivers = Trip.objects.count()
    # out_of_drivers=total_drivers - in_drivers

    # yearly_passenger = Passenger.objects.filter(date__year=current_year).count()
    # weekly_passenger = Passenger.objects.filter(date__week=current_year).count()
    # daily_passenger = Passenger.objects.filter(date=today).count()


    return render(request,'base.html', {
        'today_income': today_income,
        'year_income': year_income,
        
        # 'total_vehicles': total_vehicles,
        # 'in_service': in_service,
        # 'out_of_service': out_of_service,

        # 'total_drivers': total_drivers,
        # 'in_drivers': in_drivers,
        # 'out_of_drivers': out_of_drivers,

        # 'yearly_passenger': yearly_passenger,
        # 'weekly_passenger': weekly_passenger,
        # 'daily_passenger': daily_passenger,
    })
##################################### الصفحة الرئيسية ##################################################################


