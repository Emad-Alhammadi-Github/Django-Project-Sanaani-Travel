from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import Trip, Passenger,Nationality,Vehicle
from datetime import date
from django.db.models import Sum
from datetime import datetime
from django.db import models


#####################################  ادارة التقارير ##################################################################

# @login_required(login_url='login')
def report_view(request):
    selected_year = request.GET.get("year", datetime.now().year)
    selected_year = int(selected_year)

    # المركبات
    active_vehicles = Vehicle.objects.filter(status="in_service").count()
    stopped_vehicles = Vehicle.objects.filter(status="out_of_service").count()
    total_vehicles = Vehicle.objects.count()
    most_used_vehicle = Trip.objects.values("vehicle_type__name").annotate(count=models.Count("vehicle_type")).order_by("-count").first()

    internal_trips = Trip.objects.filter(trip_category__name="داخلية", date__year=selected_year).count()
    external_trips = Trip.objects.filter(trip_category__name="خارجية", date__year=selected_year).count()
    private_trips = Trip.objects.filter(trip_category__name="خاصة", date__year=selected_year).count()
    truck_trips = Trip.objects.filter(trip_category__name="شاحنات", date__year=selected_year).count()

    monthly_income = Trip.objects.filter(date__year=selected_year).aggregate(models.Sum("seat_price"))["seat_price__sum"] or 0
    # mid_year_income = monthly_income * 6
    # full_year_income = monthly_income * 12
    # total_income = full_year_income 

    
    # monthly_income = Passenger.objects.filter(trip_date__year=selected_year).aggregate(
    #     total_income=Sum('paid_amount')
    # )['total_income'] or 0

    mid_year_income = monthly_income * 6

    # mid_year_income = Passenger.objects.filter(
    #     trip_date__year=selected_year, trip_date__month__lte=6
    # ).aggregate(total_income=Sum('paid_amount'))['total_income'] or 0


    full_year_income = monthly_income * 12

    # full_year_income = Passenger.objects.filter(
    #     trip_date__year=selected_year
    # ).aggregate(total_income=Sum('paid_amount'))['total_income'] or 0


    total_income = full_year_income
    # total_income = Passenger.objects.aggregate(
    #     total_income=Sum('paid_amount')
    # )['total_income'] or 0


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
    }

    return render(request, 'dashboard/Reports.html', context)



# def generate_report_pdf(request):
#     selected_year = request.GET.get("year", datetime.now().year)
#     selected_year = int(selected_year)

#     # المركبات
#     active_vehicles = Vehicle.objects.filter(status="in_service").count()
#     stopped_vehicles = Vehicle.objects.filter(status="out_of_service").count()
#     total_vehicles = Vehicle.objects.count()
#     most_used_vehicle = Trip.objects.values("vehicle_type__name").annotate(count=models.Count("vehicle_type")).order_by("-count").first()

#     internal_trips = Trip.objects.filter(trip_category__name="داخلية", date__year=selected_year).count()
#     external_trips = Trip.objects.filter(trip_category__name="خارجية", date__year=selected_year).count()
#     private_trips = Trip.objects.filter(trip_category__name="خاصة", date__year=selected_year).count()
#     truck_trips = Trip.objects.filter(trip_category__name="شاحنات", date__year=selected_year).count()

#     monthly_income = Trip.objects.filter(date__year=selected_year).aggregate(models.Sum("seat_price"))["seat_price__sum"] or 0
#     mid_year_income = monthly_income * 6
#     full_year_income = monthly_income * 12
#     total_income = full_year_income
   
#     # جمع البيانات الخاصة بالتقرير
#     context = {
#         "selected_year": selected_year,
#         "monthly_income": monthly_income,
#         "mid_year_income": mid_year_income,
#         "full_year_income": full_year_income,
#         "total_income": total_income,
#         "internal_trips": internal_trips,
#         "external_trips": external_trips,
#         "private_trips": private_trips,
#         "truck_trips": truck_trips,
#         "active_vehicles": active_vehicles,
#         "stopped_vehicles": stopped_vehicles,
#         "total_vehicles": total_vehicles,
#         "most_used_vehicle": most_used_vehicle["vehicle_type__name"] if most_used_vehicle else "N/A",
#     }
    
#     # تحويل القالب إلى HTML
#     html_content = render_to_string('dashboard/report_template.html', context)

#     # تحويل HTML إلى PDF باستخدام WeasyPrint
#     pdf_file = weasyprint.HTML(string=html_content).write_pdf()

#     # إرسال PDF كاستجابة
#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="annual_report.pdf"'

#     return response








# def report_view(request):
#     # الحصول على السنة من طلب GET، أو استخدام السنة الحالية
#     selected_year = request.GET.get('year', date.today().year)

#     # جلب البيانات بناءً على السنة المحددة
#     monthly_income = Passenger.objects.filter(trip_date__year=selected_year).aggregate(
#         total_income=Sum('paid_amount')
#     )['total_income'] or 0

#     mid_year_income = Passenger.objects.filter(
#         trip_date__year=selected_year, trip_date__month__lte=6
#     ).aggregate(total_income=Sum('paid_amount'))['total_income'] or 0

#     full_year_income = Passenger.objects.filter(
#         trip_date__year=selected_year
#     ).aggregate(total_income=Sum('paid_amount'))['total_income'] or 0

#     total_income = Passenger.objects.aggregate(
#         total_income=Sum('paid_amount')
#     )['total_income'] or 0

#     # جلب بيانات الرحلات
#     # internal_trips = Trip.objects.filter(
#     #     trip_type="داخلية", trip_date__year=selected_year
#     # ).count()

#     # external_trips = Trip.objects.filter(
#     #     trip_type="خارجية", trip_date__year=selected_year
#     # ).count()

#     # private_trips = Trip.objects.filter(
#     #     trip_type="خاصة", trip_date__year=selected_year
#     # ).count()

#     # truck_trips = Trip.objects.filter(
#     #     trip_type="شاحنات", trip_date__year=selected_year
#     # ).count()

#     # جلب بيانات المركبات
#     # active_vehicles = Vehicle.objects.filter(status="فعالة").count()
#     # stopped_vehicles = Vehicle.objects.filter(status="موقفة").count()
#     # total_vehicles = Vehicle.objects.count()
#     # most_used_vehicle = Vehicle.objects.order_by('-usage_count').first()

#     # إرسال البيانات إلى القالب
#     context = {
#         'selected_year': selected_year,
#         'monthly_income': monthly_income,
#         'mid_year_income': mid_year_income,
#         'full_year_income': full_year_income,
#         'total_income': total_income,
#         # 'internal_trips': internal_trips,
#         # 'external_trips': external_trips,
#         # 'private_trips': private_trips,
#         # 'truck_trips': truck_trips,
#         # 'active_vehicles': active_vehicles,
#         # 'stopped_vehicles': stopped_vehicles,
#         # 'total_vehicles': total_vehicles,
#         # 'most_used_vehicle': most_used_vehicle.name if most_used_vehicle else "لا يوجد بيانات",
#     }
#     return render(request, 'dashboard/Reports.html', context)



#####################################  ادارة التقارير ##################################################################