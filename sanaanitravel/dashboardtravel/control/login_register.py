from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Employee,User,Nationality
import random


def login_view(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # messages.success(request, "تم تسجيل الدخول بنجاح")
                return redirect("home")
            else:
                messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة")
        
        elif form_type == "register":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if User.objects.filter(username=username).exists():
                messages.error(request, "اسم المستخدم موجود بالفعل")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "البريد الإلكتروني مستخدم بالفعل")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                                # إنشاء سجل الموظف ببيانات افتراضية
                Employee.objects.create(
                    user=user,
                    nationality=Nationality.objects.first(),  # تحديد أول جنسية في قاعدة البيانات
                
                )
                user.save()
                messages.success(request, "تم إنشاء الحساب بنجاح، يمكنك تسجيل الدخول الآن")
                return redirect("login")

    return render(request, "home/Register.html")



# def register(request):
#     return render(request, 'home/Register.html')



# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
            
#             try:
#                 employee = user.employee 
#                 request.session['user_type'] = employee.user_type
#                 request.session['user_id'] = user.id
#                 if employee.user_type == 'admin':
#                     return redirect('trip_list') 
#                 else:
#                     return redirect('home')
                
#             except Employee.DoesNotExist:
#                 messages.error(request, "المستخدم ليس موظفًا مسجلًا في النظام.")
#                 return redirect('login')
                
#         else:
#             messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")
#             return redirect('login')
#     else:
#         return render(request, 'home/Register.html')



def generate_otp():
    return random.randint(100000, 999999)



def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # phone = request.POST.get('phone')
        email = request.POST.get("email")
        try:
            employee = Employee.objects.filter(user__username=username, user__email=email).first()
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['user_id'] = employee.user.id
            messages.success(request, f"رمز التحقق الخاص بك هو: {otp}")
            return redirect('verify_otp')
        except Employee.DoesNotExist:
            messages.error(request, "اسم المستخدم أو البريد الالكتروني غير صحيح.")
            return redirect('forgot_password')

    return render(request, 'home/forgot_password.html')



def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if str(otp) == str(request.session.get('otp')):
            return redirect('reset_password')
        else:
            messages.error(request, "رمز التحقق غير صحيح.")
    return render(request, 'home/verify_otp.html')



def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            messages.success(request, "تم تغيير كلمة المرور بنجاح.")
            return redirect('login')
        else:
            messages.error(request, "كلمتا المرور غير متطابقتين.")
    return render(request, 'home/reset_password.html')



# @login_required
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('home')
