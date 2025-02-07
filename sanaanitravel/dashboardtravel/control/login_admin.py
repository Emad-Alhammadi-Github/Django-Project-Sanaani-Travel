from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Employee,User
import random


# def register_admin(request):
#     return render(request, 'dashboard/Register.html')



def login_view_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            try:
                employee = user.employee 
                request.session['user_type'] = employee.user_type
                request.session['user_id'] = user.id
                if employee.user_type == 'admin':
                    return redirect('home_dashboardtt') 
                else:
                    return redirect('home_dashboardtt')
                
            except Employee.DoesNotExist:
                messages.error(request, "المستخدم ليس موظفًا مسجلًا في النظام.")
                return redirect('login')
                
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")
            return redirect('login')
    else:
        return render(request, 'dashboard/Register.html')



def generate_otp_admin():
    return random.randint(100000, 999999)



# def forgot_password(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         phone = request.POST.get('phone')
#         try:
#             employee = Employee.objects.get(user__username=username, phone=phone)
#             otp = generate_otp_admin()
#             request.session['otp'] = otp
#             request.session['user_id'] = employee.user.id
#             messages.success(request, f"رمز التحقق الخاص بك هو: {otp}")
#             return redirect('verify_otp')
#         except Employee.DoesNotExist:
#             messages.error(request, "اسم المستخدم أو رقم الهاتف غير صحيح.")
#             return redirect('forgot_password')

#     return render(request, 'home/forgot_password.html')



# def verify_otp_admin(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         if str(otp) == str(request.session.get('otp')):
#             return redirect('reset_password')
#         else:
#             messages.error(request, "رمز التحقق غير صحيح.")
#     return render(request, 'home/verify_otp.html')



# def reset_password_admin(request):
#     if request.method == 'POST':
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')
#         if new_password == confirm_password:
#             user_id = request.session.get('user_id')
#             user = User.objects.get(id=user_id)
#             user.set_password(new_password)
#             user.save()
#             messages.success(request, "تم تغيير كلمة المرور بنجاح.")
#             return redirect('login')
#         else:
#             messages.error(request, "كلمتا المرور غير متطابقتين.")
#     return render(request, 'home/reset_password.html')



# @login_required
def logout_view_admin(request):
    logout(request)
    request.session.flush()
    return redirect('loginadmin')
