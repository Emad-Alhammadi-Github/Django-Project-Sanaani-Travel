from django.shortcuts import render, get_object_or_404, redirect
from ..models import Employee,Nationality
from django.db.models import Q
import os
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

#####################################  ادارة الموظفين ##################################################################
@login_required(login_url='login')
def employee_list(request):
    query = request.GET.get('q', '')
    employees = Employee.objects.filter(Q(name__icontains=query) | Q(phone__icontains=query))
    nationalities = Nationality.objects.all() 
    return render(request, 'dashboard/Employee.html', {'employees': employees,'nationalities': nationalities, 'query': query})

@login_required(login_url='login')
def employee_detail(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    return render(request, 'dashboard/Employee_detail.html', {'employee': employee})

@login_required(login_url='login')
def add_employee(request):
    if request.method == 'POST':
        nationality_id = request.POST.get('nationality')
        nationality = get_object_or_404(Nationality, id=nationality_id) 
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')


        user = User.objects.create_user(username=username, email=email, password=password)
        print(request.POST['name'])
        new_employee = Employee(
            user=user,
            name=request.POST['name'],
            job_title=request.POST['job_title'],
            phone=request.POST['phone'],
            id_number=request.POST['id_number'],
            salary=request.POST['salary'],
            gender=request.POST['gender'],
            nationality=nationality,
            image=request.FILES['image']
        )
        new_employee.save()
        return redirect('employee_list') 

    return render(request, 'dashboard/Employee.html')



@login_required(login_url='login')
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    nationality_id = request.POST.get('nationality')
    nationality = get_object_or_404(Nationality, id=nationality_id) 
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')


    user = User.objects.create_user(username=username, email=email, password=password)
    if request.method == 'POST':
        employee.user=user
        employee.name = request.POST['name']
        employee.job_title = request.POST['job_title']
        employee.phone = request.POST['phone']
        employee.id_number = request.POST['id_number']
        employee.salary = request.POST['salary']
        employee.gender = request.POST['gender']
        employee.nationality = nationality
        if request.FILES.get('image'):
            employee.image = request.FILES['image']
        employee.save()
        return redirect('employee_list')
    nationalities = Nationality.objects.all()
    return render(request, 'dashboard/Employee.html', {'employee': employee,'nationalities': nationalities,})


@login_required(login_url='login')
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
      if employee.image:
        if os.path.isfile(employee.image.path):
            os.remove(employee.image.path)
      employee.delete()
      return redirect('employee_list')
    return render(request, 'dashboard/Employee.html', {'employee': employee})


#####################################  ادارة الموظفين ##################################################################