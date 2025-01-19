from django.shortcuts import render, get_object_or_404, redirect
from ..models import Trip, Passenger,Nationality,ReservationRequest
from decimal import Decimal
from django.http import JsonResponse


def checkout(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    nationalities = Nationality.objects.all() 
    if request.method == 'POST':
        nationality_id = request.POST.get('nationality') 
        nationality = get_object_or_404(Nationality, id=nationality_id)
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        passport_number = request.POST.get('passport_number')
        phone = request.POST.get('phone')
        paid_amount = request.POST.get('paid_amount')
        trip_date = request.POST.get('trip_date')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')



        passengers_count = Passenger.objects.filter(trip_location=trip).count()
        if passengers_count >= trip.seat_count:
            return JsonResponse({'error': 'No seats available for this trip.'}, status=400)

        seat_number = passengers_count + 1


        seat_price = trip.seat_price

        paid_amount_decimal = Decimal(paid_amount) if paid_amount else Decimal(0)
        remaining_amount = seat_price - paid_amount_decimal  

        passenger = Passenger(
            name=name,
            id_number=id_number,
            passport_number=passport_number,
            phone=phone,
            trip_location_id=trip.id,
            paid_amount=paid_amount_decimal,
            remaining_amount=remaining_amount,
            trip_date=trip.date,
            seat_number=seat_number,
            gender=gender,
            nationality=nationality,
            image=image,
        )
        passenger.save()
        reservation_request = ReservationRequest.objects.create(passenger=passenger)
        reservation_request = ReservationRequest(passenger=passenger)
        reservation_request.save() 
        return redirect('success_page')
    
    return render(request, 'home/checkOut.html', {'trip': trip,'nationalities': nationalities})