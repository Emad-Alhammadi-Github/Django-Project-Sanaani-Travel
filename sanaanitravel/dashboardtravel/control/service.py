from django.shortcuts import render, get_object_or_404, redirect
from ..models import Service
from django.db.models import Q
import os
from django.contrib.auth.decorators import login_required


# @login_required(login_url='login')
# def service_list(request):
#     query = request.GET.get('q', '')
#     services = Service.objects.filter(Q(name__icontains=query))
#     return render(request, 'trips/service_list.html', {'services': services, 'query': query})

@login_required(login_url='login')
def add_service(request):
    if request.method == 'POST':
        service = Service(
            name=request.POST['name'],
            service_type=request.POST['service_type'],
            description=request.POST['description'],
            image=request.FILES['image']
        )
        service.save()
        return redirect('trip_list')
    return render(request, 'dashboard/Trips.html')



# @login_required(login_url='login')
# def edit_service(request, service_id):
#     service = get_object_or_404(Service, id=service_id)
#     if request.method == 'POST':
#         service.name = request.POST['name']
#         service.service_type = request.POST['service_type']
#         service.description = request.POST['description']
#         if 'image' in request.FILES:
#             service.image = request.FILES['image']
#         service.save()
#         return redirect('service_list')
#     return render(request, 'trips/edit_service.html', {'service': service})


# @login_required(login_url='login')
# def delete_service(request, service_id):
#     service = get_object_or_404(Service, id=service_id)
#     if request.method == 'POST':
#        if service.image:
#          if os.path.isfile(service.image.path):
#               os.remove(service.image.path)
#        service.delete()
#        return redirect('service_list')
#     return render(request, 'trips/delete_service.html', {'service': service})