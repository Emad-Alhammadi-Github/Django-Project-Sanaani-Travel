from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# from ..models import Trip, Passenger,Nationality,Vehicle,City,ReservationRequest
from datetime import date
from datetime import datetime
from django.db import models
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.contrib import messages
#####################################  ادارة التقارير ##################################################################
from django.shortcuts import render
from django.db.models import Q, Sum, Count, Avg, F, ExpressionWrapper, FloatField
from datetime import datetime
from ..models import *





def calculate_income(trips_query):

    monthly_income = trips_query.aggregate(total_income=Sum("seat_price"))["total_income"] or 0
    mid_year_income = monthly_income * 6
    full_year_income = monthly_income * 12
    return monthly_income, mid_year_income, full_year_income

def filter_passengers(passengers, filters):

    return passengers.filter(**filters)

@login_required(login_url='login')
def reports_view(request):

    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    

    querysets = {
        'trips': Trip.objects.all(),
        'passengers': Passenger.objects.all(),
        'vehicles': Vehicle.objects.all(),
        'drivers': Driver.objects.all(),
        'invoices': Invoice.objects.all(),
        'private_trips': PrivateTripRequest.objects.all(),
        'employees': Employee.objects.all(),
        'nationalities': Nationality.objects.all(),
        'cities': City.objects.all(),
        'travel_types': TravelType.objects.all(),
        'trip_categories': TripCategory.objects.all(),
    }
    
    # تطبيق الفلاتر
    if search_query:
        for name, qs in querysets.items():
            if name == 'trips':
                querysets[name] = qs.filter(
                    Q(departure__name__icontains=search_query) |
                    Q(destination__name__icontains=search_query) |
                    Q(travel_type__name__icontains=search_query) |
                    Q(trip_category__name__icontains=search_query) |
                    Q(vehicle_type__name__icontains=search_query) |
                    Q(details__icontains=search_query)
                )
            elif name == 'passengers':
                querysets[name] = qs.filter(
                    Q(name__icontains=search_query) |
                    Q(id_number__icontains=search_query) |
                    Q(passport_number__icontains=search_query) |
                    Q(phone__icontains=search_query) |
                    Q(nationality__name__icontains=search_query) |
                    Q(trip_location__departure__name__icontains=search_query) |
                    Q(trip_location__destination__name__icontains=search_query)
                )
            elif name == 'vehicles':
                querysets[name] = qs.filter(
                    Q(name__icontains=search_query) |
                    Q(plate_number__icontains=search_query) |
                    Q(model__icontains=search_query) |
                    Q(driver__name__icontains=search_query)
                )
            elif name == 'drivers':
                querysets[name] = qs.filter(
                    Q(name__icontains=search_query) |
                    Q(phone__icontains=search_query) |
                    Q(license_number__icontains=search_query) |
                    Q(id_number__icontains=search_query) |
                    Q(nationality__name__icontains=search_query)
                )
            elif name == 'invoices':
                querysets[name] = qs.filter(
                    Q(passenger__name__icontains=search_query) |
                    Q(trip__departure__name__icontains=search_query) |
                    Q(trip__destination__name__icontains=search_query) |
                    Q(payment_method__icontains=search_query)
                )
            elif name == 'private_trips':
                querysets[name] = qs.filter(
                    Q(customer_name__icontains=search_query) |
                    Q(departure__name__icontains=search_query) |
                    Q(destination__name__icontains=search_query) |
                    Q(customer_phone__icontains=search_query) |
                    Q(status__icontains=search_query)
                )
            elif name == 'employees':
                querysets[name] = qs.filter(
                    Q(name__icontains=search_query) |
                    Q(job_title__icontains=search_query) |
                    Q(phone__icontains=search_query) |
                    Q(id_number__icontains=search_query) |
                    Q(nationality__name__icontains=search_query)
                )

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            date_filters = {
                'trips': ('date', [start_date, end_date]),
                'passengers': ('date_added__date', [start_date, end_date]),
                'vehicles': ('date_added__date', [start_date, end_date]),
                'drivers': ('date_added__date', [start_date, end_date]),
                'invoices': ('date_added__date', [start_date, end_date]),
                'private_trips': ('trip_date', [start_date, end_date]),
                'employees': ('date_added__date', [start_date, end_date]),
            }
            
            for name, (field, date_range) in date_filters.items():
                querysets[name] = querysets[name].filter(**{f'{field}__range': date_range})
                
        except ValueError:
            pass
    

    total_passengers = querysets['passengers'].count()
    total_trips = querysets['trips'].count()
    total_invoices = querysets['invoices'].count()
    

    stats = {

        'financial_summary': {
            'total_invoices': querysets['invoices'].aggregate(
                total_paid=Sum('paid_amount'),
                total_remaining=Sum('remaining_amount'),
                total_amount=Sum('total_amount'),
                count=Count('id')
            ),
            'monthly_financial': querysets['invoices'].values(
                'date_add__month', 'date_add__year'
            ).annotate(
                total_paid=Sum('paid_amount'),
                total_remaining=Sum('remaining_amount'),
                count=Count('id')
            ).order_by('date_add__year', 'date_add__month'),
            'payment_methods': querysets['invoices'].values(
                'payment_method'
            ).annotate(
                count=Count('id'),
                total=Sum('total_amount')
            ).order_by('-count'),
        },
        

        'trips_stats': {
            'by_type': querysets['trips'].values(
                'travel_type__name'
            ).annotate(
                count=Count('id'),
                avg_seats=Avg('seat_count'),
                avg_price=Avg('seat_price')
            ).annotate(
                percentage=ExpressionWrapper(
                    100.0 * F('count') / total_trips if total_trips > 0 else 0,
                    output_field=FloatField()
                )
            ),
            'by_category': querysets['trips'].values(
                'trip_category__name'
            ).annotate(
                count=Count('id')
            ).annotate(
                percentage=ExpressionWrapper(
                    100.0 * F('count') / total_trips if total_trips > 0 else 0,
                    output_field=FloatField()
                )
            ),
            'by_vehicle': querysets['trips'].values(
                'vehicle_type__name'
            ).annotate(
                count=Count('id')
            ).annotate(
                percentage=ExpressionWrapper(
                    100.0 * F('count') / total_trips if total_trips > 0 else 0,
                    output_field=FloatField()
                )
            ),
            'by_route': querysets['trips'].values(
                'departure__name', 'destination__name'
            ).annotate(
                count=Count('id')
            ).order_by('-count')[:10],
            'total': total_trips,
        },
        

        'passengers_stats': {
            'by_nationality': querysets['passengers'].values(
                'nationality__name'
            ).annotate(
                count=Count('id')
            ).annotate(
                percentage=ExpressionWrapper(
                    100.0 * F('count') / total_passengers if total_passengers > 0 else 0,
                    output_field=FloatField()
                )
            ).order_by('-count'),
            'by_gender': querysets['passengers'].values(
                'gender'
            ).annotate(
                count=Count('id')
            ).annotate(
                percentage=ExpressionWrapper(
                    100.0 * F('count') / total_passengers if total_passengers > 0 else 0,
                    output_field=FloatField()
                )
            ),
            'by_departure_city': querysets['passengers'].values(
                'trip_location__departure__name',
                'trip_location__departure__nationality__name'
            ).annotate(
                count=Count('id')
            ).annotate(
                percentage=ExpressionWrapper(
                    100.0 * F('count') / total_passengers if total_passengers > 0 else 0,
                    output_field=FloatField()
                )
            ).order_by('-count'),
            'by_arrival_city': querysets['passengers'].values(
                'trip_location__destination__name',
                'trip_location__destination__nationality__name'
            ).annotate(
                count=Count('id')
            ).annotate(
                percentage=ExpressionWrapper(
                    100.0 * F('count') / total_passengers if total_passengers > 0 else 0,
                    output_field=FloatField()
                )
            ).order_by('-count'),
            'total': total_passengers,
             'all_passengers': querysets['passengers'].order_by('-date_added'),
        },
        

        'vehicles_stats': {
            'by_type': querysets['vehicles'].values(
                'vehicle_type'
            ).annotate(
                count=Count('id'),
                avg_capacity=Avg('passenger_capacity')
            ),
            'by_status': querysets['vehicles'].values(
                'status'
            ).annotate(
                count=Count('id')
            ),
            'by_driver': querysets['vehicles'].values(
                'driver__name'
            ).annotate(
                count=Count('id')
            ).order_by('-count')[:5],

            'all_vehicles': querysets['vehicles'].order_by('-date_added')
        },

        'drivers_stats': {
            'by_type': querysets['drivers'].values(
                'driver_type'
            ).annotate(
                count=Count('id')
            ),
            'by_nationality': querysets['drivers'].values(
                'nationality__name'
            ).annotate(
                count=Count('id')
            ).order_by('-count'),
            'by_experience': querysets['drivers'].values(
                'experience_years'
            ).annotate(
                count=Count('id')
            ).order_by('experience_years'),

            'all_drivers': querysets['drivers'].order_by('-date_added')
        },

        'private_trips_stats': {
            'by_status': querysets['private_trips'].values(
                'status'
            ).annotate(
                count=Count('id')
            ),
            'by_route': querysets['private_trips'].values(
                'departure__name', 'destination__name'
            ).annotate(
                count=Count('id')
            ).order_by('-count')[:5],
            'by_vehicle': querysets['private_trips'].values(
                'vehicle_type__name'
            ).annotate(
                count=Count('id')
            ),
        },
        

        'employees_stats': {
            'by_position': querysets['employees'].values(
                'job_title'
            ).annotate(
                count=Count('id'),
                avg_salary=Avg('salary')
            ),
            'by_nationality': querysets['employees'].values(
                'nationality__name'
            ).annotate(
                count=Count('id')
            ),
            'by_gender': querysets['employees'].values(
                'gender'
            ).annotate(
                count=Count('id')
            ),
            'all_employees': querysets['employees'].select_related('nationality').order_by('-date_added')
        },
    }
    



    current_year = datetime.now().year  


    user_entered_dates = bool(start_date or end_date)

    if user_entered_dates:

        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
            

            filter_year = start_date_obj.year if start_date_obj else (end_date_obj.year if end_date_obj else current_year)
            

            trips_query = querysets["trips"].filter(date_added__year=filter_year)
            date_filter = {"trip_location__date_added__year": filter_year}
            

            start_date = datetime(filter_year, 1, 1).date()
            end_date = datetime(filter_year, 12, 31).date()
            
        except ValueError:

            filter_year = current_year
            trips_query = querysets["trips"].filter(date_added__year=filter_year)
            date_filter = {"trip_location__date_added__year": filter_year}
            start_date = datetime(filter_year, 1, 1).date()
            end_date = datetime(filter_year, 12, 31).date()
    else:

        filter_year = current_year
        trips_query = querysets["trips"].filter(date_added__year=filter_year)
        date_filter = {"trip_location__date_added__year": filter_year}
        start_date = datetime(filter_year, 1, 1).date()
        end_date = datetime(filter_year, 12, 31).date()


    monthly_income, mid_year_income, full_year_income = calculate_income(trips_query)
    total_income = full_year_income


    print(f"عدد الرحلات : {trips_query.count()}")
    today = date.today()

    if start_date or end_date:

        try:

            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
            

            if start_date and end_date:
                trips_query = querysets["trips"].filter(date_added__date__range=(start_date, end_date))
                date_filter = {"trip_location__date_added__date__range": [start_date, end_date]}
            elif start_date:
                trips_query = querysets["trips"].filter(date_added__date=start_date)
                date_filter = {"trip_location__date_added__date": start_date}
            elif end_date:
                trips_query = querysets["trips"].filter(date_added__date=end_date)
                date_filter = {"trip_location__date_added__date": end_date}
                
        except ValueError:

            start_date = today
            end_date = today
            trips_query = querysets["trips"].filter(date_added__date=today)
            date_filter = {"trip_location__date_added__date": today}
    else:
   
        start_date = today
        end_date = today
        trips_query = querysets["trips"].filter(date_added__date=today)
        date_filter = {"trip_location__date_added__date": today}


    daily_income = trips_query.aggregate(total_income=Sum("seat_price"))["total_income"] or 0


    internal_passengers = filter_passengers(querysets["passengers"], {
        "trip_location__departure__nationality__name": "اليمن",
        "trip_location__destination__nationality__name": "اليمن",
        **date_filter
    })
    is_yemeni_trip = internal_passengers.aggregate(total_paid=Sum("paid_amount"))["total_paid"] or 0

    external_passengers = querysets["passengers"].exclude(
        trip_location__departure__nationality__name="اليمن",
        trip_location__destination__nationality__name="اليمن"
    ).filter(**date_filter)
    is_no_yemeni_trip = external_passengers.aggregate(total_paid=Sum("paid_amount"))["total_paid"] or 0

    private_passengers = filter_passengers(querysets["passengers"], {
        "trip_location__trip_category__name__icontains": "خاصة",
        **date_filter
    })
    is_private_trip = private_passengers.aggregate(total_paid=Sum("paid_amount"))["total_paid"] or 0

    truck_passengers = filter_passengers(querysets["passengers"], {
        "trip_location__trip_category__name__icontains": "عامة",
        **date_filter
    })
    is_truck_trip = truck_passengers.aggregate(total_paid=Sum("paid_amount"))["total_paid"] or 0



    internal_invoices = Invoice.objects.filter(
        trip__is_internal=True,
        date_add=today,
        status='paid'  
    )
    internal_income = internal_invoices.aggregate(
        total=Sum('paid_amount')
    )['total'] or 0
    

    external_invoices = Invoice.objects.filter(
        trip__is_internal=False,
        date_add=today,
        status='paid'
    )
    external_income = external_invoices.aggregate(
        total=Sum('paid_amount')
    )['total'] or 0
    

    private_invoices = Invoice.objects.filter(
        trip__trip_category__name__icontains='خاصة',
        date_add=today,
        status='paid'
    )
    private_income = private_invoices.aggregate(
        total=Sum('paid_amount')
    )['total'] or 0
    

    public_invoices = Invoice.objects.filter(
        trip__trip_category__name__icontains='عامة',
        date_add=today,
        status='paid'
    )
    public_income = public_invoices.aggregate(
        total=Sum('paid_amount')
    )['total'] or 0
    

    private_trip_payments = PrivateTripPayment.objects.filter(
        payment_date__date=today,
        status='paid'
    )
    private_trip_income = private_trip_payments.aggregate(
        total=Sum('amount')
    )['total'] or 0
    

    total_incomerr = (internal_income + external_income + 
                   private_income + public_income + 
                   private_trip_income)




    context = {
        'querysets': querysets,
        'stats': stats,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'current_year': current_year,




    'user_specified_dates': user_entered_dates,  
    'filter_year': filter_year,
    'financial_report': {
        'monthly_income': monthly_income,
        'mid_year_income': mid_year_income,
        'full_year_income': full_year_income,
        'total_income': total_income,
        'is_annual_report': not user_entered_dates, 
    },
        'today': today,
        'daily_income': daily_income,
        'is_yemeni_trip': is_yemeni_trip,
        'is_no_yemeni_trip': is_no_yemeni_trip,
        'is_private_trip': is_private_trip,
        'is_truck_trip': is_truck_trip,


        'internal_income': internal_income,
        'external_income': external_income,
        'private_income': private_income + private_trip_income,  
        'public_income': public_income,
        'total_incomerr': total_incomerr,
        'internal_invoices_count': internal_invoices.count(),
        'external_invoices_count': external_invoices.count(),
        'private_invoices_count': private_invoices.count(),
        'public_invoices_count': public_invoices.count(),
        'private_trip_payments_count': private_trip_payments.count(),
    }
    
    return render(request, 'dashboard/Reports.html', context)







# @login_required(login_url='login')

# def calculate_income(trips_query):

#     monthly_income = trips_query.aggregate(total_income=Sum("seat_price"))["total_income"] or 0
#     mid_year_income = monthly_income * 6
#     full_year_income = monthly_income * 12
#     return monthly_income, mid_year_income, full_year_income

# def filter_passengers(passengers, filters):

#     return passengers.filter(**filters)

# def report_view(request):
#     trips = Trip.objects.all()
#     passengers = Passenger.objects.all()

#     selected_date = request.GET.get("year")
#     current_year = datetime.now().year  

#     if selected_date:
#         selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
#         selected_year = selected_date.year  
#         selected_month = selected_date.month  
#         trips_query = trips.filter(date_added__year=selected_year, date_added__month=selected_month)  
#     else:
#         selected_date = None
#         selected_year = current_year  
#         selected_month = datetime.now().month  
#         trips_query = trips.filter(date_added__year=selected_year, date_added__month=selected_month) 

#     monthly_income, mid_year_income, full_year_income = calculate_income(trips_query)
#     total_income = full_year_income

#     # if selected_year == current_year:
        
#     #     monthly_income, mid_year_income, full_year_income = calculate_income(trips_query)
#     # else:
#     #     monthly_income, mid_year_income, full_year_income = 0, 0, 0


#     print(f"عدد الرحلات : {trips_query.count()}")

#     total_income_check = trips_query.aggregate(total_income=Sum("seat_price"))["total_income"]
#     print(f"إجمالي الدخل: {total_income_check}")


#     internal_passengers = filter_passengers(passengers, {
#         "trip_location__departure__nationality__name": "اليمن",
#         "trip_location__destination__nationality__name": "اليمن",
#         "trip_location__date_added__date" if selected_date else "trip_location__date_added__year": selected_date if selected_date else selected_year
#     })
#     is_yemeni_trip = internal_passengers.aggregate(total_paid=Sum("paid_amount"))["total_paid"] or 0

#     external_passengers = passengers.exclude(
#         trip_location__departure__nationality__name="اليمن",
#         trip_location__destination__nationality__name="اليمن"
#     ).filter(**{
#         "trip_location__date_added__date" if selected_date else "trip_location__date_added__year": selected_date if selected_date else selected_year
#     })
#     is_no_yemeni_trip = external_passengers.aggregate(total_paid=Sum("paid_amount"))["total_paid"] or 0

#     private_passengers = filter_passengers(passengers, {
#         "trip_location__trip_category__name__icontains": "خاصة",
#         "trip_location__date_added__date" if selected_date else "trip_location__date_added__year": selected_date if selected_date else selected_year
#     })
#     is_private_trip = private_passengers.aggregate(total_paid=Sum("paid_amount"))["total_paid"] or 0

#     truck_passengers = filter_passengers(passengers, {
#         "trip_location__trip_category__name__icontains": "عامة",
#         "trip_location__date_added__date" if selected_date else "trip_location__date_added__year": selected_date if selected_date else selected_year
#     })
#     is_truck_trip = truck_passengers.aggregate(total_paid=Sum("paid_amount"))["total_paid"] or 0

#     internal_trips = trips_query.filter(is_internal=True).count()
#     external_trips = trips_query.filter(is_internal=False).count()
#     private_trips = trips_query.filter(trip_category__name__icontains="خاصة").count()
#     truck_trips = trips_query.filter(trip_category__name__icontains="عامة").count()

#     total_passengers_internal = internal_passengers.count()
#     total_passengers_external = external_passengers.count()
#     total_passengers_private = private_passengers.count()
#     total_passengers_public = truck_passengers.count()

#     total_vehicles = Vehicle.objects.count()
#     active_vehicles = trips_query.values("vehicle_type__name").annotate(count=Count("vehicle_type")).count()
#     stopped_vehicles = total_vehicles - active_vehicles

#     most_used_vehicle = trips_query.values("vehicle_type__name").annotate(count=Count("vehicle_type")).order_by("-count").first()

#     vehicles_internal = Vehicle.objects.filter(
#         trip__is_internal=True,
#         **{"trip__date_added__date" if selected_date else "trip__date_added__year": selected_date if selected_date else selected_year}
#     ).distinct().count()
#     vehicles_external = Vehicle.objects.filter(
#         trip__is_internal=False,
#         **{"trip__date_added__date" if selected_date else "trip__date_added__year": selected_date if selected_date else selected_year}
#     ).distinct().count()

#     accepted_reservations = ReservationRequest.objects.filter(
#         status="approved",
#         **{"passenger__trip_location__date_added__date" if selected_date else "passenger__trip_location__date_added__year": selected_date if selected_date else selected_year}
#     ).count()
#     rejected_reservations = ReservationRequest.objects.filter(
#         status="rejected",
#         **{"passenger__trip_location__date_added__date" if selected_date else "passenger__trip_location__date_added__year": selected_date if selected_date else selected_year}
#     ).count()

#     nationality_report = []
#     if selected_date:
#         for nationality in Nationality.objects.filter(cities__departures__date_added__date=selected_date).distinct():
#             nationality_trips = trips_query.filter(departure__nationality=nationality)
#             nationality_passengers = Passenger.objects.filter(trip_location__in=nationality_trips).count()
#             nationality_report.append({
#                 'name': nationality.name,
#                 'trips': nationality_trips.count(),
#                 'passengers': nationality_passengers,
#             })
#     else:
#         for nationality in Nationality.objects.all():
#             nationality_trips = trips.filter(departure__nationality=nationality)
#             nationality_passengers = Passenger.objects.filter(trip_location__in=nationality_trips).count()
#             nationality_report.append({
#                 'name': nationality.name,
#                 'trips': nationality_trips.count(),
#                 'passengers': nationality_passengers,
#             })

#     city_report = []
#     if selected_date:
#         for city in City.objects.filter(departures__date_added__date=selected_date).distinct():
#             trip_count = trips_query.filter(departure=city).count()
#             passenger_count = Passenger.objects.filter(trip_location__departure=city).count()
#             city_report.append({
#                 'city_name': city.name,
#                 'trip_count': trip_count,
#                 'passenger_count': passenger_count,
#             })
#     else:
#         for city in City.objects.all():
#             trip_count = trips.filter(departure=city).count()
#             passenger_count = Passenger.objects.filter(trip_location__departure=city).count()
#             city_report.append({
#                 'city_name': city.name,
#                 'trip_count': trip_count,
#                 'passenger_count': passenger_count,
#             })

#     context = {
#         "is_yemeni_trip": is_yemeni_trip,
#         "is_no_yemeni_trip": is_no_yemeni_trip,
#         "is_private_trip": is_private_trip,
#         "is_truck_trip": is_truck_trip,
#         "selected_date": selected_date,
#         "selected_year": selected_year, 
#         "monthly_income": monthly_income,
#         "mid_year_income": mid_year_income,
#         "full_year_income": full_year_income,
#         "total_income": total_income,
#         "internal_trips": internal_trips,
#         "external_trips": external_trips,
#         "private_trips": private_trips,
#         "truck_trips": truck_trips,
#         'vehicles_internal': vehicles_internal,
#         'vehicles_external': vehicles_external,
#         'total_passengers_internal': total_passengers_internal,
#         'total_passengers_external': total_passengers_external,
#         'total_passengers_private': total_passengers_private,
#         'total_passengers_public': total_passengers_public,
#         'accepted_reservations': accepted_reservations,
#         'rejected_reservations': rejected_reservations,
#         "active_vehicles": active_vehicles,
#         "stopped_vehicles": stopped_vehicles,
#         "total_vehicles": total_vehicles,
#         'nationality_report': nationality_report,
#         'city_report': city_report,
#         "most_used_vehicle": most_used_vehicle["vehicle_type__name"] if most_used_vehicle else "N/A",
#         "nationalities": Nationality.objects.all(),
#         "cities": City.objects.all(),
#     }

#     return render(request, 'dashboard/Reports.html', context)


def get_cities(request):
    nationality_id = request.GET.get('nationality_id')
    cities = City.objects.filter(nationality_id=nationality_id).values('id', 'name')
    return JsonResponse({'cities': list(cities)})
#####################################  ادارة التقارير ##################################################################


