from django.shortcuts import render, get_object_or_404, redirect
from ..models import Driver,Nationality
from django.db.models import Q
import os
from django.contrib.auth.decorators import login_required

#####################################  ادارة السواقين ##################################################################

@login_required(login_url='login')
def driver_list(request):
    query = request.GET.get('q', '')
    drivers = Driver.objects.filter(Q(name__icontains=query) | Q(phone__icontains=query))
    nationalities = Nationality.objects.all() 
    return render(request,'dashboard/Drivers.html', {'drivers': drivers,'nationalities': nationalities, 'query': query})

@login_required(login_url='login')
def driver_detail(request, driver_id):
    driver = Driver.objects.get(id=driver_id)
    return render(request, 'dashboard/Drivers_detail.html', {'driver': driver})

@login_required(login_url='login')
def add_driver(request):
    if request.method == 'POST':
        nationality_id = request.POST.get('nationality') 
        nationality = get_object_or_404(Nationality, id=nationality_id) 
        driver = Driver(
            name=request.POST['name'],
            experience_years=request.POST['experience_years'],
            phone=request.POST['phone'],
            license_type=request.POST['license_type'],
            license_number=request.POST['license_number'],
            id_number=request.POST['id_number'],
            passport_number=request.POST['passport_number'],
            gender=request.POST['gender'],
            nationality=nationality,
            image=request.FILES['image']
        )
        driver.save()
        return redirect('driver_list')
    return render(request, 'dashboard/Drivers.html')



@login_required(login_url='login')
def edit_driver(request,driver_id):
    driver = get_object_or_404(Driver, id=driver_id)

    if request.method == 'POST':
        nationality_id = request.POST.get('nationality') 
        nationality = get_object_or_404(Nationality, id=nationality_id) 
        driver.name = request.POST['name']
        driver.experience_years = request.POST['experience_years']
        driver.phone = request.POST['phone']
        driver.license_type = request.POST['license_type']
        driver.license_number = request.POST['license_number']
        driver.id_number = request.POST['id_number']
        driver.passport_number = request.POST['passport_number']
        driver.gender = request.POST['gender']
        driver.nationality = nationality
        
        if 'image' in request.FILES and request.FILES['image']:
            driver.image = request.FILES['image']
        driver.save()
        return redirect('driver_list')

    return render(request, 'dashboard/Drivers.html', {'driver': driver})


@login_required(login_url='login')
def delete_driver(request,driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    if request.method == 'POST':
        if driver.image:
            if os.path.isfile(driver.image.path):
                os.remove(driver.image.path)
        driver.delete() 
        return redirect('driver_list') 
    return redirect('driver_list') 

#####################################  ادارة السواقين ##################################################################