from django.db.models import Prefetch, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from ..models import  PrivateTripRequest, PrivateTripApproval, PrivateTripPayment,Nationality, City
from ..forms import PrivateTripRequestForm, TripApprovalForm, PaymentForm
from django.http import JsonResponse

@login_required
def request_private_trip(request):
    if request.method == 'POST':
        form = PrivateTripRequestForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.customer = request.user
            

            yemen = Nationality.objects.filter(name='اليمن').first()
            if (yemen and 
                trip.departure.nationality == yemen and 
                trip.destination.nationality == yemen):
                trip.customer_passport_number = None  
            
            trip.save()
            return redirect('success_page')
    else:
        form = PrivateTripRequestForm()
    
    return render(request, 'home/request_trip.html', {'form': form})

def check_cities(request):
    departure_id = request.GET.get('departure')
    destination_id = request.GET.get('destination')
    
    try:
        yemen = Nationality.objects.get(name='اليمن')
        departure = City.objects.get(id=departure_id)
        destination = City.objects.get(id=destination_id)
        

        both_in_yemen = (departure.nationality == yemen and 
                        destination.nationality == yemen)
        
        return JsonResponse({
            'hide_passport': both_in_yemen,
            'departure': departure.name,
            'destination': destination.name
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    






# def request_private_trip(request):
#     if request.method == 'POST':
#         form = PrivateTripRequestForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(form.cleaned_data)  
#             trip = form.save(commit=False)
#             trip.customer = request.user
#             trip.save()
#             print("تم حفظ الرحلة بنجاح!") 
#             return redirect('private_trip_status', trip_id=trip.id)
#         else:
#             print("أخطاء النموذج:", form.errors)
#     else:
#         form = PrivateTripRequestForm()
    
#     return render(request, 'home/request_trip.html', {'form': form})

@login_required
def private_trip_status(request, trip_id):
    trip = get_object_or_404(PrivateTripRequest, id=trip_id, customer=request.user)
    return render(request, 'home/trip_status.html', {'trip': trip})

@login_required
def my_private_trips(request):
    trips = PrivateTripRequest.objects.filter(customer=request.user).order_by('-created_at')
    print(trips)
    return render(request, 'home/trip_status.html', {'trips': trips})

@login_required(login_url='loginadmin')
def manage_private_trips(request):
    trips = PrivateTripRequest.objects.all().order_by('-created_at')
    status = request.GET.get('status')
    
    if status:
        trips = trips.filter(status=status)
    
    return render(request, 'dashboard/manage_trips.html', {'trips': trips})



@login_required(login_url='loginadmin')
def approve_private_trip(request, trip_id):
    trip = get_object_or_404(PrivateTripRequest, id=trip_id)
    
    if request.method == 'POST':
        form = TripApprovalForm(request.POST)
        if form.is_valid():
            approval = form.save(commit=False)
            approval.trip_request = trip
            approval.approved_by = request.user
            approval.save()
            
            trip.status = 'approved'
            trip.save()
            
            return redirect('manage_private_trips')
    else:
        form = TripApprovalForm(initial={'price': calculate_trip_price(trip)})
    
    return render(request, 'dashboard/approve_trip.html', {
        'trip': trip,
        'form': form
    })

@login_required(login_url='loginadmin')
def reject_private_trip(request, trip_id):
    trip = get_object_or_404(PrivateTripRequest, id=trip_id)
    trip.status = 'rejected'
    trip.save()
    return redirect('manage_private_trips')

@login_required
def make_payment(request, trip_id):
    trip = get_object_or_404(PrivateTripRequest, id=trip_id, customer=request.user)
    
    if not hasattr(trip, 'approval'):
        return redirect('private_trip_status', trip_id=trip_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.trip_request = trip
            payment.amount = trip.approval.price

            payment.save()
            payment.status = 'paid'
            payment.save()
            
            trip.status = 'completed'
            trip.save()
            
            return redirect('my_private_trips')
    else:
        form = PaymentForm()
    
    return render(request, 'home/make_payment.html', {
        'trip': trip,
        'form': form
    })

# @login_required
# def payment_confirmation(request, payment_id):
#     payment = get_object_or_404(PrivateTripPayment, id=payment_id, trip_request__customer=request.user)
#     return render(request, 'home/payment_confirmation.html', {'payment': payment})

def calculate_trip_price(trip):
    base_price = 100
    distance_factor = 1.5 
    passenger_factor = trip.passenger_count * 0.2
    return base_price * distance_factor * passenger_factor