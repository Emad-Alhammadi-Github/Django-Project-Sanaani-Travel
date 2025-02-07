from django.shortcuts import render, get_object_or_404, redirect
from ..models import Trip, Passenger,Nationality,ReservationRequest
from decimal import Decimal
from django.http import JsonResponse
from datetime import datetime




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
        date_of_birth=request.POST.get('date_of_birth')



        passengers_count = Passenger.objects.filter(trip_location=trip).count()
        if passengers_count >= trip.seat_count:
            
            return redirect('error_checkOut')

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
            date_of_birth=date_of_birth,

        )
        passenger.save()
        reservation_request = ReservationRequest.objects.create(passenger=passenger)
        reservation_request.save() 

        request.session['passenger_name'] = passenger.name
        request.session['paid_amount'] = str(passenger.paid_amount)
        request.session['remaining_amount'] = str(passenger.remaining_amount)
        return redirect('success_page')

    
    return render(request, 'home/checkOut.html', {'trip': trip,'nationalities': nationalities})





# def checkout(request, trip_id):
#     trip = get_object_or_404(Trip, id=trip_id)
#     nationalities = Nationality.objects.all() 
#     if request.method == 'POST':
#         nationality_id = request.POST.get('nationality') 
#         nationality = get_object_or_404(Nationality, id=nationality_id)
#         name = request.POST.get('name')
#         id_number = request.POST.get('id_number')
#         passport_number = request.POST.get('passport_number')
#         phone = request.POST.get('phone')
#         paid_amount = request.POST.get('paid_amount')
#         gender = request.POST.get('gender')
#         image = request.FILES.get('image')

#         # التحقق من وجود مقاعد شاغرة
#         passengers_count = Passenger.objects.filter(trip_location=trip).count()
#         if passengers_count >= trip.seat_count:
#             return JsonResponse({'error': 'No seats available for this trip.'}, status=400)

#         seat_number = passengers_count + 1

#         # حساب المبلغ المدفوع والمبلغ المتبقي
#         seat_price = trip.seat_price
#         paid_amount_decimal = Decimal(paid_amount) if paid_amount else Decimal(0)
#         remaining_amount = seat_price - paid_amount_decimal  

#         # حفظ الحجز في جدول ReservationRequest مع حالة 'pending'
#         reservation_request = ReservationRequest(
#             passenger=None,  # سيتم تعيين المسافر بعد الموافقة
#             request_date=datetime.now().date(),
#             status='pending'
#         )
#         reservation_request.save()

#         # حفظ بيانات الحجز في جدول المسافر بعد الموافقة
#         passenger = Passenger(
#             name=name,
#             id_number=id_number,
#             passport_number=passport_number,
#             phone=phone,
#             trip_location=trip,
#             paid_amount=paid_amount_decimal,
#             remaining_amount=remaining_amount,
#             seat_number=seat_number,
#             gender=gender,
#             nationality=nationality,
#             image=image
#         )
#         passenger.save()

#         reservation_request.passenger = passenger
#         reservation_request.save()

#         return redirect('reservation_requests')  

#     return render(request, 'home/checkOut.html', {'trip': trip, 'nationalities': nationalities})