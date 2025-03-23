from django.shortcuts import render, get_object_or_404, redirect
from ..models import Trip, Passenger, Invoice,ReservationRequest,Vehicle
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Q
#####################################  ادارة الفواتير ##################################################################

#صفحة عرض الفواتير
@login_required(login_url='loginadmin')
def invoice_list(request):
    query = request.GET.get('q', '')

    invoices = Invoice.objects.filter(
        Q(passenger__name__icontains=query)
    ).prefetch_related(
        Prefetch(
            'passenger__reservation_requests',
            queryset=ReservationRequest.objects.filter(status='approved'),
            to_attr='approved_reservations'
        )
    )

    trips = Trip.objects.all()
    passengers = Passenger.objects.all()

    for invoice in invoices:
        if invoice.passenger.approved_reservations:
            invoice.reservation_date = invoice.passenger.approved_reservations[0].request_date
        else:
            invoice.reservation_date = None
    return render(request, 'dashboard/Bills.html', {
        'invoices': invoices,
        'trips': trips,
        'passengers': passengers,
        'query': query,
    })



#صفحة اضافة فاتورة
@login_required(login_url='loginadmin')
def add_invoice(request):
    if request.method == 'POST':
        invoice = Invoice(
            passenger=Passenger.objects.get(id=request.POST['passenger']),
            paid_amount=request.POST['paid_amount'],
            remaining_amount=request.POST['remaining_amount'],
            trip=Trip.objects.get(id=request.POST['trip']),
            
            seat_number=request.POST['seat_number'],
            total_amount=request.POST['total_amount'],
            payment_method=request.POST['payment_method'],
            status=request.POST['status'],
        )
        invoice.save()
        return redirect('invoice_list')
    
    passengers = Passenger.objects.all()
    vehicles = Vehicle.objects.all()
    trips = Trip.objects.all()
    return render(request, 'dashboard/Bills.html', {'passengers': passengers, 'trips': trips, 'vehicles': vehicles})



@login_required(login_url='loginadmin')
def edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == 'POST':
        invoice.passenger = Passenger.objects.get(id=request.POST['passenger'])
        invoice.paid_amount = request.POST['paid_amount']
        invoice.remaining_amount = request.POST['remaining_amount']
        invoice.trip = Trip.objects.get(id=request.POST['trip'])
        invoice.seat_number = request.POST['seat_number']
        invoice.total_amount = request.POST['total_amount']
        invoice.save()
        return redirect('invoice_list')
    passengers = Passenger.objects.all()
    trips = Trip.objects.all()
    return render(request, 'trips/edit_invoice.html', {'invoice': invoice, 'passengers': passengers, 'trips': trips})



@login_required(login_url='loginadmin')
def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_list')
    return render(request, 'trips/delete_invoice.html', {'invoice': invoice})
#####################################  ادارة الفواتير ##################################################################