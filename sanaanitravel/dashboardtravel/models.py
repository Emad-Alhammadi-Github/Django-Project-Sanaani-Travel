from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Nationality(models.Model):
    name = models.CharField(max_length=100, unique=True)  

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE, related_name='cities') 

    def __str__(self):
        return self.name


class TravelType(models.Model):
    name = models.CharField(max_length=50, unique=True) 

    def __str__(self):
        return self.name

class TripCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

#### السواقين
class Driver(models.Model):
    driver_type= models.CharField(max_length=20, choices=[('tocompany', 'تابع لشركة'), ('tobe', 'تابع لجهه'), ('drivername', 'سواق')], default='drivername')
    name = models.CharField(max_length=100)  # الاسم
    experience_years = models.IntegerField(null=True, blank=True)  # سنوات الخبرة
    phone = models.CharField(max_length=15,null=True)  # الهاتف
    license_type = models.CharField(max_length=50,null=True)  # نوع رخصة القيادة
    license_number = models.CharField(max_length=50,null=True)  # رقم رخصة القيادة
    license_img = models.ImageField(upload_to='driver/license_img/', null=True, blank=True)  # مسار صورة رخصة القيادة للسائق

    id_number = models.CharField(max_length=50,null=True)  # رقم البطاقة الشخصية
    identify_img =models.ImageField(upload_to='driver/identify_img/', null=True, blank=True)   # مسار صورة الهوية الوطنية للسائق

    passport_number = models.CharField(max_length=50,null=True)  # رقم جواز السفر
    gender = models.CharField(max_length=10,null=True)  # الجنس
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE, related_name='cities_driver',null=True)  #   الجنسية
    image = models.ImageField(upload_to='driver/driver_images/', null=True, blank=True)  # صورة
    date_of_birth = models.DateField(null=True, blank=True)  # تاريخ ميلاد السائق
    date_added = models.DateTimeField(auto_now_add=True)  # التاريخ والوقت
    date_add = models.DateField(auto_now_add=True) # التاريخ انشاء السواق

    def __str__(self):
        return self.name

### المركبات
class Vehicle(models.Model):
    name = models.CharField(max_length=100)  # اسم السيارة
    vehicle_type = models.CharField(max_length=50)  # نوع السيارة   
    model = models.CharField(max_length=50,null=True)  # الموديل
    plate_number = models.CharField(max_length=20)  # رقم اللوحة
    status = models.CharField(max_length=20,null=True)  # الحالة
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # سعر السيارة
    # owner = models.CharField(max_length=100,null=True)  # لمن تابعة
    passenger_capacity = models.IntegerField()  # عدد الركاب
    date_added = models.DateTimeField(auto_now_add=True)  # التاريخ والوقت
    fuel_capacity = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # سعة البنزين
    motor_type=models.CharField(max_length=50,null=True)
    # driver =  models.ManyToManyField(Driver)  # السائق
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)  # السائق
    description = models.TextField(null=True)  # وصف السيارة
    image = models.ImageField(upload_to='vehicle/vehicle_images/', null=True, blank=True)  # صورة
    img1 = models.ImageField(upload_to='vehicle/', null=True, blank=True)  # صورة أولى للمركبة (اختياري)
    date_add = models.DateField(auto_now_add=True) # التاريخ انشاء المركبة

    def __str__(self):
        return self.name

    
### الرحلات
class Trip(models.Model):
    departure = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departures')  # السفر من (المحافظة)
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='destinations')  # السفر إلى (المحافظة)
    travel_type = models.ForeignKey(TravelType, on_delete=models.CASCADE)  # نوع السفر
    trip_category = models.ForeignKey(TripCategory, on_delete=models.CASCADE)  # نوع الرحلة
    vehicle_type = models.ForeignKey(Vehicle, on_delete=models.CASCADE)  # نوع السيارة
    # driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trips')  # السائق
    date = models.DateField()  # تاريخ الرحلة        
    time = models.TimeField()  # الوقت
    seat_count = models.IntegerField()  # عدد المقاعد
    seat_price = models.DecimalField(max_digits=10, decimal_places=2)  # سعر المقعد
    details = models.TextField(null=True)  # تفاصيل الرحلة
    image = models.ImageField(upload_to='trip_images/', null=True, blank=True)  # صورة
    date_added = models.DateTimeField(auto_now_add=True)  # التاريخ والوقت انشاء الرحلة
    date_add = models.DateField(auto_now_add=True) # التاريخ انشاء الرحلة
    is_internal = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.departure} to {self.destination} on {self.date}"





### الموظفين
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True)  # الاسم
    job_title = models.CharField(max_length=50,null=True)  # المسمى الوظيفي
    phone = models.CharField(max_length=15,null=True)  # الهاتف
    id_number = models.CharField(max_length=50,null=True)  # رقم البطاقة الشخصية
    salary = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # الراتب
    gender = models.CharField(max_length=10,null=True)  # الجنس
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE, related_name='cities_employee')  #   الجنسية
    image = models.ImageField(upload_to='employee_images/', null=True, blank=True)  # صورة
    user_type = models.CharField(max_length=20, choices=[('admin', 'أدمن'), ('manger', 'مدير'), ('employee', 'موظف'), ('mangertrip', 'مسوول الرحلات'),('mangerpassenger', 'مسوول المسافرين'),('manmonay', 'المسوول المالي'),  ('customer', 'عميل')], default='customer')
    date_added = models.DateTimeField(auto_now_add=True)  # التاريخ والوقت
    date_add = models.DateField(auto_now_add=True) # التاريخ انشاء الموظف



### المسافرين
class Passenger(models.Model):
    name = models.CharField(max_length=100)  # الاسم
    id_number = models.CharField(max_length=50)  # رقم البطاقة الشخصية
    identify_img = models.ImageField(upload_to='passenger/identify_img/', null=True, blank=True)  # مسار صورة الهوية الوطنية للراكب

    passport_number = models.CharField(max_length=50,null=True)  # رقم جواز السفر
    phone = models.CharField(max_length=15,null=True)  # الهاتف
    trip_location = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='passengers')  # مكان الرحلة    
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)  # المدفوع
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)  # المتبقي
    # trip_date = models.DateField()  # تاريخ الرحلة
    seat_number = models.IntegerField()  # المقعد
    gender = models.CharField(max_length=10,null=True)  # الجنس
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE, related_name='cities_passenger')  #  الجنسية
    image = models.ImageField(upload_to='passenger/passenger_images/', null=True, blank=True)  # صورة
    # date_of_birth = models.DateField(null=True)  # تاريخ ميلاد الراكب
    date_added = models.DateTimeField(auto_now_add=True)  # التاريخ والوقت
    date_add = models.DateField(auto_now_add=True) # التاريخ انشاء المسافر
    def __str__(self):
        return self.name


class ReservationRequest(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='reservation_requests')  # المسافر
    request_date = models.DateField(auto_now_add=True)  # تاريخ الطلب
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )  # حالة الطلب

    def __str__(self):
        return f"Reservation for {self.passenger.name} - {self.get_status_display()}"
    

### الفواتير
class Invoice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),          
        ('paid', 'Paid'),                
        ('overdue', 'Overdue'),        
        ('cancelled', 'Cancelled'),      
     ]
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)  # المسافر
    # reservationrequest = models.ForeignKey(ReservationRequest, on_delete=models.CASCADE)  # المسافر
    # type_vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)  # نوع السيارة
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)  # المدفوع
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)  # المتبقي
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)  # الرحلة
    seat_number = models.IntegerField()  # المقعد
    # trip_date = models.DateField()  # تاريخ الرحلة
    # time = models.TimeField()  # الوقت
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # المجموع
    payment_method = models.CharField(max_length=15,null=True)  # طريقة الدفع

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')  # حالة الفاتورة
    date_added = models.DateTimeField(auto_now_add=True)  # التاريخ والوقت
    date_add = models.DateField(auto_now_add=True) # التاريخ انشاء الفاتورة




class PrivateTripRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('approved', 'تم الموافقة'),
        ('rejected', 'تم الرفض'),
        ('completed', 'مكتملة'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='private_trips')
    trip_type = models.ForeignKey(TravelType, on_delete=models.CASCADE)
    departure = models.ForeignKey(City, on_delete=models.CASCADE, related_name='private_departures')
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='private_destinations')
    vehicle_type = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    passenger_count = models.IntegerField()
    trip_date = models.DateField()
    trip_time = models.TimeField()
    special_requests = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    customer_name = models.CharField(max_length=100)
    customer_id_number = models.CharField(max_length=50) 
    identify_img = models.ImageField(upload_to='passenger/identify_img/', null=True, blank=True)
    customer_passport_number = models.CharField(max_length=50,null=True) 
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField(null=True, blank=True)
    customer_nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"رحلة خاصة من {self.departure.name} إلى {self.destination.name} - {self.get_status_display()}"

class PrivateTripApproval(models.Model):
    trip_request = models.OneToOneField(PrivateTripRequest, on_delete=models.CASCADE, related_name='approval')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approved_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"موافقة على الرحلة {self.trip_request.id}"

class PrivateTripPayment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'قيد الانتظار'),
        ('paid', 'تم الدفع'),
        ('failed', 'فشل الدفع'),
    ]
    
    trip_request = models.ForeignKey(PrivateTripRequest, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"دفع {self.amount} لرحلة {self.trip_request.id}"








class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)  # الفاتورة المرتبطة بالدفع
    payment_date = models.DateTimeField(auto_now_add=True)  # تاريخ الدفع
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # المبلغ المدفوع
    transfer_number = models.CharField(max_length=50, blank=True, null=True)  # رقم الحوالة (اختياري)
    proof_document = models.CharField(max_length=200, blank=True, null=True)  # مستند إثبات الدفع (اختياري)
    proof_document_img = models.ImageField(upload_to='payment/proof_document_img/', null=True, blank=True)   # مستند إثبات الدفع (اختياري)
    verified = models.BooleanField(default=False)  # حالة التحقق من الدفع


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    
### الخدمات
class Service(models.Model):
    name = models.CharField(max_length=100)  # الاسم
    service_type = models.CharField(max_length=50)  # النوع
    description = models.TextField()  # الوصف
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)  # صورة
