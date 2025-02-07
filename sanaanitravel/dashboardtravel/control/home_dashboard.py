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
    
    return render(request,'base.html', {
        'today_income': today_income,
        'year_income': year_income,
        
    })

def home_dashboardtt(request):
    return render(request,'base.html')
##################################### الصفحة الرئيسية ##################################################################


