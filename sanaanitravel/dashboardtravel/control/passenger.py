from django.shortcuts import render, get_object_or_404, redirect
from ..models import Trip, Passenger,Nationality
from django.db.models import Q
from decimal import Decimal
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
#####################################  ادارة المسافرين ##################################################################

#صفحة عرض المسافرين
@login_required(login_url='loginadmin')
def passenger_list(request):
    query = request.GET.get('q', '')
    passengers = Passenger.objects.filter(Q(name__icontains=query) | Q(phone__icontains=query) | Q(paid_amount__icontains=query) | Q(remaining_amount__icontains=query) | Q(date_added__icontains=query))
    trips = Trip.objects.all()  
    nationalities = Nationality.objects.all() 
    return render(request, 'dashboard/Passenger.html', {'passengers': passengers, 'trips': trips,'nationalities': nationalities, 'query': query})
#صفحة تفاصيل المسافر
@login_required(login_url='loginadmin')
def passenger_detail(request, passenger_id):
    passenger = Passenger.objects.get(id=passenger_id)
    return render(request, 'dashboard/Passenger_detail.html', {'passenger': passenger})


#صفحة اضافة مسافر
@login_required(login_url='loginadmin')
def add_passenger(request):
    if request.method == 'POST':
        nationality_id = request.POST.get('nationality') 
        nationality = get_object_or_404(Nationality, id=nationality_id)
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        passport_number = request.POST.get('passport_number')
        phone = request.POST.get('phone')
        trip_location_id = request.POST.get('trip_location')
        paid_amount = request.POST.get('paid_amount')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')
        identify_img = request.FILES.get('identify_img')
        print(image)

        trip = Trip.objects.get(id=trip_location_id)


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
            trip_location_id=trip_location_id,
            paid_amount=paid_amount_decimal,
            remaining_amount=remaining_amount,
            seat_number=seat_number,
            gender=gender,
            nationality=nationality,
            image=image,
            identify_img=identify_img,
        )
        passenger.save()
        return redirect('passenger_list')

    trips = Trip.objects.all() 
    nationalities = Nationality.objects.all()
    return render(request, 'dashboard/Passenger.html', {'trips': trips,'nationalities': nationalities}) 

#صفحة تعديل مسافر
@login_required(login_url='loginadmin')
def edit_passenger(request,passenger_id):
    passenger = get_object_or_404(Passenger, id=passenger_id)
    nationality_id = request.POST.get('nationality') 
    nationality = get_object_or_404(Nationality, id=nationality_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        passport_number = request.POST.get('passport_number')
        phone = request.POST.get('phone')
        trip_location_id = request.POST.get('trip_location')
        paid_amount = request.POST.get('paid_amount')
        gender = request.POST.get('gender')
        image = request.FILES.get('image') 
        identify_img = request.FILES.get('identify_img')
        print("111111111111111111111111111")
        print("111111111111111111111111111")

        trip = Trip.objects.get(id=trip_location_id)
        
        
        
        seat_price = trip.seat_price

        remaining_amount = seat_price - Decimal(paid_amount)




        passenger.name = name
        passenger.id_number = id_number
        passenger.passport_number = passport_number
        passenger.phone = phone
        passenger.trip_location_id = trip_location_id
        passenger.paid_amount = paid_amount
        passenger.remaining_amount = remaining_amount
        passenger.gender = gender
        passenger.nationality = nationality
        
        if image:
            if passenger.image:
                old_image_path = os.path.join(settings.MEDIA_ROOT, str(passenger.image))
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)
            passenger.image = image 

        if identify_img:
            if passenger.identify_img:
                old_identify_img_path = os.path.join(settings.MEDIA_ROOT, str(passenger.identify_img))
                if os.path.isfile(old_identify_img_path):
                    os.remove(old_identify_img_path)
            passenger.identify_img = identify_img 
        passenger.save()

        return redirect('passenger_list')  

    nationalities = Nationality.objects.all()
    return render(request, 'dashboard/Passenger.html', {'passenger': passenger,'nationalities': nationalities,})


#صفحة تعديل معاملة مالية لمسافر
def transction_payment_passenger(request, passenger_id):
    passenger = get_object_or_404(Passenger, id=passenger_id)
    if request.method == 'POST':
        additional_payment = request.POST.get('additional_payment')
        if additional_payment:
            paid_amo=passenger.paid_amount + Decimal(additional_payment)
            remaining_amo=passenger.remaining_amount - Decimal(additional_payment)

        passenger.paid_amount = paid_amo
        passenger.remaining_amount = remaining_amo
        passenger.save()
        return redirect('passenger_list')  





#حذف مسافر
@login_required(login_url='loginadmin')
def delete_passenger(request, passenger_id):
    passenger = get_object_or_404(Passenger, id=passenger_id)
    if request.method == 'POST':
        if passenger.image:
            if os.path.isfile(passenger.image.path):
                os.remove(passenger.image.path)

        passenger.delete()
        return redirect('passenger_list')
    return redirect('passenger_list')


#####################################  ادارة المسافرين ##################################################################