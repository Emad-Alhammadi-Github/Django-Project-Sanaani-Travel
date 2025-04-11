from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from ..models import Driver, Vehicle
from django.db.models import Q
import os
from django.contrib.auth.decorators import login_required
#####################################  ادارة المركبات ##################################################################

@login_required(login_url='loginadmin')
def vehicle_list(request):
    query = request.GET.get('q', '')
    vehicles = Vehicle.objects.filter(Q(name__icontains=query) | Q(plate_number__icontains=query))
    for vehicle in vehicles:
        vehicle.fuel_capacity = float(vehicle.fuel_capacity) 
        vehicle.price = float(vehicle.price)
        print(vehicle.fuel_capacity, vehicle.price)
    drivers = Driver.objects.all()
    return render(request, 'dashboard/Vehicle.html', {'vehicles': vehicles, 'drivers': drivers, 'query': query})



@login_required(login_url='loginadmin')
def vehicle_detail(request, vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    return render(request, 'dashboard/Vehicle_detail.html', {'vehicle': vehicle})




@login_required(login_url='loginadmin')
def add_vehicle(request):
    if request.method == 'POST':
 
        price = request.POST.get('price', '0') or '0'
        fuel_capacity = request.POST.get('fuel_capacity', '0') or '0'
        
        try:
            vehicle = Vehicle(
                name=request.POST['name'],
                vehicle_type=request.POST['vehicle_type'],
                model=request.POST.get('model'),
                plate_number=request.POST['plate_number'],
                status=request.POST.get('status'),
                price=Decimal(price),  
                passenger_capacity=request.POST['passenger_capacity'],
                motor_type=request.POST.get('motor_type'),
                fuel_capacity=Decimal(fuel_capacity),  
                description=request.POST.get('description', ''),
                driver=Driver.objects.get(id=request.POST['driver']),
            )
            
  
            if 'image' in request.FILES:
                vehicle.image = request.FILES['image']
            if 'img1' in request.FILES:
                vehicle.img1 = request.FILES['img1']
            
            vehicle.save()
            return redirect('vehicle_list')
            
        except Exception as e:
    
            print(f"Error: {e}")
    
            return render(request, 'dashboard/Vehicle.html', {'error': str(e)})

    return render(request, 'dashboard/Vehicle.html')





@login_required(login_url='loginadmin')
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        vehicle.name = request.POST['name']
        vehicle.vehicle_type = request.POST['vehicle_type']
        vehicle.model = request.POST['model']
        vehicle.plate_number = request.POST['plate_number']
        vehicle.status = request.POST['status']
        vehicle.price = request.POST['price']
        # vehicle.owner = request.POST['owner']
        vehicle.passenger_capacity = request.POST['passenger_capacity']
        vehicle.motor_type = request.POST['motor_type']
        vehicle.fuel_capacity = request.POST['fuel_capacity']
        vehicle.description = request.POST['description']
        vehicle.driver = Driver.objects.get(id=request.POST['driver'])
        if 'image' in request.FILES:
            vehicle.image = request.FILES['image']

        if 'img1' in request.FILES:
            vehicle.img1 = request.FILES['img1']
        vehicle.save()
        return redirect('vehicle_list')
    drivers = Driver.objects.all()
    return render(request, 'dashboard/Vehicle.html', {'vehicle': vehicle, 'drivers': drivers})



@login_required(login_url='loginadmin')
def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
      if vehicle.image:
        if os.path.isfile(vehicle.image.path):
            os.remove(vehicle.image.path)
      vehicle.delete()
      return redirect('vehicle_list')
    return render(request, 'dashboard/Vehicle.html', {'vehicle': vehicle})
#####################################  ادارة المركبات ##################################################################