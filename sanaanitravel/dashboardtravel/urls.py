from django.urls import path
from . import views
from dashboardtravel.control.trip import *
from dashboardtravel.control.passenger import *
from dashboardtravel.control.employee import *
from dashboardtravel.control.driver import *
from dashboardtravel.control.vehicle import *
from dashboardtravel.control.bill import *
from dashboardtravel.control.report import *
from dashboardtravel.control.home import *
from dashboardtravel.control.service import *
from dashboardtravel.control.home_dashboard import *
from dashboardtravel.control.login_register import *
from dashboardtravel.control.checkOut import *
from dashboardtravel.control.reservation import *

urlpatterns = [
#####################################   الرئيسية ##################################################################
    path('', home, name='home'),
    path('dashboard', home_dashboard, name='home_dashboard'),
    path('checkout/<int:trip_id>/', checkout, name='checkout'),
    path('success/', success_page, name='success_page'),
    path('error_checkOut/', error_checkOut, name='error_checkOut'),
    path('search/', search_trips, name='search_trips'),

#####################################   الرئيسية النهاية ##################################################################




#####################################   التسجيل / تسجيل الدخول ##################################################################

    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('reset-password/', reset_password, name='reset_password'),
    path('logout/', logout_view, name='logout'),


#####################################   التسجيل / تسجيل الدخول النهاية ##################################################################




#####################################  ادارة الرحلات ##################################################################
    path('trip/', trip_list, name='trip_list'),
    path('trip/filter/', trip_filter, name='trip_filter'),
    path('trips/add/', add_trip, name='add_trip'),
    path('edit_trip/', edit_trip, name='edit_trip'),
    path('trip_detail/<int:trip_id>/', trip_detail, name='trip_detail'),
    path('delete_trip/', delete_trip, name='delete_trip'),
    # path('trips/edit/<int:trip_id>/', edit_trip, name='edit_trip'),
    # path('trips/delete/<int:trip_id>/', delete_trip, name='delete_trip'),

    path('service/add/', add_service, name='add_service'),
#####################################  ادارة الرحلات النهاية ##################################################################





#####################################  ادارة المسافرين ##################################################################
    path('passenger/', passenger_list, name='passenger_list'),
    path('passenger/add/', add_passenger, name='add_passenger'),
    path('edit_passenger/<int:passenger_id>/', edit_passenger, name='edit_passenger'),
    path('passenger_detail/<int:passenger_id>/', passenger_detail, name='passenger_detail'),
    path('transction_payment_passenger/<int:passenger_id>/', transction_payment_passenger, name='transction_payment_passenger'),

    path('delete_passenger/<int:passenger_id>/', delete_passenger, name='delete_passenger'),

#####################################  ادارة المسافرين النهاية ##################################################################




#####################################  ادارة الطلبات ##################################################################
    path('reservation-requests/', reservation_requests, name='reservation_requests'),
    path('approve-reservation/<int:reservation_id>/', approve_reservation, name='approve_reservation'),
    path('reject-reservation/<int:reservation_id>/', reject_reservation, name='reject_reservation'),
#####################################  ادارة الطلبات النهاية##################################################################



#####################################  ادارة الموظفين ##################################################################
    path('employee/', employee_list, name='employee_list'),
    path('add_employee/', add_employee, name='add_employee'),
    path('edit_employee/<int:employee_id>/', edit_employee, name='edit_employee'),
    path('employee_detail/<int:employee_id>/', employee_detail, name='employee_detail'),
    path('delete_employee/<int:employee_id>/', delete_employee, name='delete_employee'),
#####################################  ادارة الموظفين النهاية ##################################################################
   





#####################################  ادارة السواقين ##################################################################
    path('driver/', driver_list, name='driver_list'),
    path('add_driver/', add_driver, name='add_driver'),
    path('edit_driver/<int:driver_id>/', edit_driver, name='edit_driver'),
    path('driver_detail/<int:driver_id>/', driver_detail, name='driver_detail'),
    path('delete_driver/<int:driver_id>/', delete_driver, name='delete_driver'),
#####################################  ادارة السواقين النهاية ##################################################################






#####################################  ادارة المركبات ##################################################################
    path('vehicle/', vehicle_list, name='vehicle_list'),
    path('add_vehicle/', add_vehicle, name='add_vehicle'),
    path('edit_vehicle/<int:vehicle_id>/', edit_vehicle, name='edit_vehicle'),
    path('vehicle_detail/<int:vehicle_id>/', vehicle_detail, name='vehicle_detail'),
    path('delete_vehicle/<int:vehicle_id>/', delete_vehicle, name='delete_vehicle'),
#####################################  ادارة المركبات النهاية ##################################################################






#####################################  ادارة الفواتير ##################################################################
    path('invoices/', invoice_list, name='invoices_list'),
    path('invoice/<int:invoice_id>/update/', edit_invoice, name='update_invoice'),

#####################################  ادارة الفواتير النهاية ##################################################################






#####################################  ادارة التقارير ##################################################################
    path('report/', report_view, name='report'),


#####################################  ادارة التقارير النهاية ##################################################################



]

