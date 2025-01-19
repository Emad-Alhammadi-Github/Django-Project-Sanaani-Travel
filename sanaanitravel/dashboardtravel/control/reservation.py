from django.shortcuts import render, get_object_or_404, redirect
from ..models import Trip, Passenger,Employee,Service,Driver,Vehicle,ReservationRequest,Invoice
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def reservation_requests(request):
    reservations = ReservationRequest.objects.filter(status='pending')
    return render(request, 'dashboard/reservation_requests.html', {'reservations': reservations})

@login_required(login_url='login')
def approve_reservation(request, reservation_id):
    reservation = get_object_or_404(ReservationRequest, id=reservation_id)

    reservation.status = 'approved'
    reservation.save()
    # passenger = reservation.passenger
    # passenger.save()
    
    # الحصول على المسافر المرتبط بالحجز
    passenger = reservation.passenger
    vtt=reservation.passenger.trip_location.vehicle_type

    # إنشاء الفاتورة
    invoice = Invoice.objects.create(
        passenger=passenger,
        type_vehicle=vtt,  # افترض أن الرحلة تحتوي على مركبة
        paid_amount=passenger.paid_amount,
        remaining_amount=passenger.remaining_amount,
        trip=passenger.trip_location,
        seat_number=passenger.seat_number,
        trip_date=passenger.trip_date,
        time=passenger.trip_location.time,  # افترض أن الرحلة تحتوي على وقت
        total_amount=passenger.paid_amount + passenger.remaining_amount,  # حساب الإجمالي
    )

    # حفظ الفاتورة
    invoice.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def reject_reservation(request, reservation_id):
    reservation = get_object_or_404(ReservationRequest, id=reservation_id)
    reservation.status = 'rejected'
    reservation.save()

    # passenger_id=  reservation.passenger.id
    # passenger = get_object_or_404(Passenger, id=passenger_id)
    # passenger.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))