from django.shortcuts import render, get_object_or_404, redirect
from ..models import Trip, Passenger,Employee,Service,Driver,Vehicle,ReservationRequest,Invoice
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='loginadmin')
def reservation_requests(request):
    reservations = ReservationRequest.objects.filter(status='pending')
    return render(request, 'dashboard/reservation_requests.html', {'reservations': reservations})

@login_required(login_url='loginadmin')
def reservation_requests_priveit(request):
    reservations = ReservationRequest.objects.filter(status='pending')
    return render(request, 'dashboard/reservation_requests_priveit.html', {'reservations': reservations})
@login_required(login_url='loginadmin')
def approve_reservation_list(request):
    reservations_approved = ReservationRequest.objects.filter(status='approved')
    return render(request, 'dashboard/approve_reservation.html', {'reservations_approved': reservations_approved})


@login_required(login_url='loginadmin')
def reject_reservation_list(request):
    reservations_rejected = ReservationRequest.objects.filter(status='rejected')
    return render(request, 'dashboard/reject_reservation.html', {'reservations_rejected': reservations_rejected})


@login_required(login_url='loginadmin')
def approve_reservation(request, reservation_id):
    reservation = get_object_or_404(ReservationRequest, id=reservation_id)

    reservation.status = 'approved'
    reservation.save()

    passenger = reservation.passenger
    vtt=reservation.passenger.trip_location.vehicle_type

    invoice = Invoice.objects.create(
        passenger=passenger,
        paid_amount=passenger.paid_amount,
        remaining_amount=passenger.remaining_amount,
        trip=passenger.trip_location,
        seat_number=passenger.seat_number,
 
        total_amount=passenger.paid_amount + passenger.remaining_amount,  
    )

    invoice.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='loginadmin')
def reject_reservation(request, reservation_id):
    reservation = get_object_or_404(ReservationRequest, id=reservation_id)
    reservation.status = 'rejected'
    reservation.save()

    # passenger_id=  reservation.passenger.id
    # passenger = get_object_or_404(Passenger, id=passenger_id)
    # passenger.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='loginadmin')
def reject_reservation_delete(request, reservation_id):
    reservation = get_object_or_404(ReservationRequest, id=reservation_id)
    reservation.delete()
    passenger_id=  reservation.passenger.id
    passenger = get_object_or_404(Passenger, id=passenger_id)
    passenger.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))