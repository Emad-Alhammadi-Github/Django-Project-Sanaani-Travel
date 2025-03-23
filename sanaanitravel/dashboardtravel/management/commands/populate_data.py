from django.core.management.base import BaseCommand
from dashboardtravel.models import Nationality, City, TravelType, TripCategory,Employee,Driver,Vehicle,Trip
from django.contrib.auth.models import User
import requests
from faker import Faker
from random import choice, randint
from django.core.files.base import ContentFile
from django.core.files import File
from io import BytesIO
class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **kwargs):
        nationalities = [
            'اليمن', 'مصر', 'السعودية', 'الأردن', 'العراق',
            'فلسطين', 'سوريا', 'لبنان', 'الإمارات', 'الكويت',
        ]

        for country in nationalities:
            Nationality.objects.get_or_create(name=country)

        countries_and_cities = {
            'اليمن': [
                'صنعاء', 'عدن', 'المكلا', 'تعز', 'الحديدة',
                'البيضاء', 'إب', 'لحج', 'مأرب', 'صعدة'
            ],
            'مصر': [
                'القاهرة', 'الإسكندرية', 'الجيزة', 'أسوان', 'المنصورة',
                'طنطا', 'الزقازيق', 'قنا', 'الفيوم', 'الأقصر'
            ],
            'السعودية': [
                'الرياض', 'جدة', 'مكة', 'المدينة المنورة', 'الدمام',
                'الطائف', 'الخبر', 'الدمام', 'القطيف', 'بريدة'
            ],
            'الأردن': [
                'عمان', 'إربد', 'الزرقاء', 'المفرق', 'البتراء',
                'العقبة', 'جرش', 'مادبا', 'الكرك', 'السلط'
            ],
            'العراق': [
                'بغداد', 'البصرة', 'نينوى', 'كربلاء', 'المثنى',
                'النجف', 'السليمانية', 'ديالى', 'ذي قار', 'الأنبار'
            ],
            'فلسطين': [
                'رام الله', 'القدس', 'الخليل', 'نابلس', 'غزة',
                'جنين', 'بيت لحم', 'طولكرم', 'الناصرة', 'قلقيلية'
            ],
            'سوريا': [
                'دمشق', 'حلب', 'اللاذقية', 'طرطوس', 'حمص',
                'دير الزور', 'الرقة', 'إدلب', 'حماة', 'درعا'
            ],
            'لبنان': [
                'بيروت', 'طرابلس', 'صيدا', 'بعلبك', 'زحلة',
                'صور', 'جبيل', 'الهرمل', 'الشوف', 'عاليه'
            ],
            'الإمارات': [
                'دبي', 'أبوظبي', 'الشارقة', 'العين', 'الفجيرة',
                'رأس الخيمة', 'عجمان', 'أم القيوين', 'الظفرة'
            ],
            'الكويت': [
                'الكويت العاصمة', 'الفروانية', 'حولي', 'الأحمدي', 'مبارك الكبير',
                'الجهراء', 'المنقف', 'النعيم', 'صباح السالم'
            ]
        }

        for country, cities in countries_and_cities.items():
            nationality = Nationality.objects.get(name=country)
            for city in cities:
                City.objects.get_or_create(name=city, nationality=nationality)

        # nationalities = [
        #     'اليمن', 'مصر', 'السعودية', 'الأردن', 'العراق',
        #     'فلسطين', 'سوريا', 'لبنان', 'الإمارات', 'الكويت',
        # ]

        # for country in nationalities:
        #     Nationality.objects.get_or_create(name=country)

        # yemen_nationality = Nationality.objects.get(name='اليمن')
        # cities = [
        # 'صنعاء', 'عدن', 'المكلا', 'تعز', 'الحديدة',
        # 'البيضاء', 'إب', 'لحج', 'مأرب', 'صعدة',
 
        # ]

        # for city in cities:
        #   City.objects.get_or_create(name=city, nationality=yemen_nationality)

        travel_types = [
            'برّي', 'بحري',
        ]

        for travel_type in travel_types:
            TravelType.objects.get_or_create(name=travel_type)

        trip_categories = [
        'خاصة', 'عامة',
        ]

        for trip_category in trip_categories:
            TripCategory.objects.get_or_create(name=trip_category)


        yemen_nationality = Nationality.objects.get(name='اليمن')
        # nationality, created = Nationality.objects.get_or_create(name='يمني')

        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com', 
            password='admin123'
        )

        admin_user.is_staff = True
        admin_user.is_active = True
        admin_user.save()

        Employee.objects.create(
            user=admin_user,
            name='Admin', 
            job_title='مدير', 
            phone='123456789',
            id_number='1234567890',
            salary=10000,
            gender='1',
            user_type='admin',
            nationality=yemen_nationality,
        )
        # employee_user = User.objects.create(
        #     username='emp',
        #     email='emp@gmail.com', 
        #     password='emp123'
        # )

        # admin_user.is_active = True
        # admin_user.save()

        # Employee.objects.create(
        #     user=employee_user,
        #     name='Employee', 
        #     job_title='موظف', 
        #     phone='12345',
        #     id_number='123450',
        #     salary=10000,
        #     gender='1',
        #     user_type='employee',
        #     nationality=yemen_nationality,
        # )

        # manmonay_user = User.objects.create(
        #     username='manmon',
        #     email='manmon@gmail.com', 
        #     password='manmon123'
        # )

        # admin_user.is_active = True
        # admin_user.save()

        # Employee.objects.create(
        #     user=manmonay_user,
        #     name='Manmonay', 
        #     job_title='مسوول مالي', 
        #     phone='1234567',
        #     id_number='12345670',
        #     salary=10000,
        #     gender='1',
        #     user_type='manmonay',
        #     nationality=yemen_nationality,
        # )


    #     fake = Faker()
    #     driver_images = [self.fetch_image() for _ in range(10)]
    #     vehicle_images = [self.fetch_image_vehicle() for _ in range(10)]
    #     trip_images = [self.fetch_imagetrip() for _ in range(10)]

    #    
    #     for i in range(10):
    #         nationality = Nationality.objects.order_by('?').first()
    #         driver = Driver.objects.create(
    #             name=fake.name(),
    #             experience_years=randint(1, 20),
    #             phone=fake.phone_number(),
    #             license_type=choice(['12 راكب', '6 ركاب','16 راكب',]),
    #             license_number=fake.license_plate(),
    #             license_img=driver_images[i],
    #             id_number=fake.ssn(),
    #             identify_img=driver_images[i],
    #             passport_number=fake.passport_number(),
    #             gender=choice(['1', '0']),
    #             nationality=nationality,
    #             image=driver_images[i],
    #             date_of_birth=fake.date_of_birth(minimum_age=20, maximum_age=60),
    #         )

    #  
    #     for i in range(10):
    #         driver = Driver.objects.order_by('?').first()
    #         Vehicle.objects.create(
    #             name=fake.company() + " " + fake.word(),  # تم تعديل هنا
    #             vehicle_type=choice(['حافلة', 'باص رويشان', 'هيلوكس', 'رافور', 'كورلا', 'ليكزاز', 'مرسيدس', 'بي ام دبليو']),
    #             model=fake.word(),
    #             plate_number=fake.license_plate(),
    #             status=choice(['new', 'old', 'in_service']),
    #             price=randint(10000, 50000),
    #             owner=fake.name(),
    #             passenger_capacity=randint(1, 50),
    #             fuel_capacity=randint(30, 100),
    #             motor_type=choice(['بترول', 'ديزل', 'كهرباء','غاز']),
    #             driver=driver,
    #             description=fake.text(),
    #             image=vehicle_images[i],
    #             img1=vehicle_images[i],
    #         )

    #     
    #     for i in range(10):
    #         departure_city = City.objects.order_by('?').first()
    #         destination_city = City.objects.exclude(id=departure_city.id).order_by('?').first()
    #         vehicle = Vehicle.objects.order_by('?').first()
    #         travel_type = TravelType.objects.order_by('?').first()
    #         trip_category = TripCategory.objects.order_by('?').first()

    #         Trip.objects.create(
    #             departure=departure_city,
    #             destination=destination_city,
    #             travel_type=travel_type,
    #             trip_category=trip_category,
    #             vehicle_type=vehicle,
    #             date=fake.date(),
    #             time=fake.time(),
    #             seat_count=randint(1, 50),
    #             seat_price=randint(10, 100),
    #             details=fake.text(),
    #             image=trip_images[i],
    #         )

    #     self.stdout.write(self.style.SUCCESS('Data populated successfully.'))

    # def fetch_image(self):
    #     image_urls = [
    #         'https://www.pexels.com/photo/photography-of-a-guy-wearing-green-shirt-1222271.jpeg',  
    #     ]
    #     url = choice(image_urls)
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         return ContentFile(response.content, name=f'driver_image_{randint(1, 10000)}.jpg') 
    #     else:
    #         return ContentFile(response.content, name=f'driver_image_{randint(1, 10000)}.jpg') 
    # def fetch_image_vehicle(self):
    #     image_urls = [
    #     'https://images.pexels.com/photos/2036544/pexels-photo-2036544.jpeg',  
    #     ]
    #     url = choice(image_urls)
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         return ContentFile(response.content, name=f'vehicle_image_{randint(1, 10000)}.jpg')
    #     else:
    #         return ContentFile(response.content, name=f'vehicle_image_{randint(1, 10000)}.jpg')    

    # def fetch_imagetrip(self):
    #     image_urls = [
    #     'https://images.pexels.com/photos/30459688/pexels-photo-30459688.jpeg',  
    #     ]
    #     url = choice(image_urls)
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         return ContentFile(response.content, name=f'trip_image_{randint(1, 10000)}.jpg')
    #     else:
    #         return ContentFile(response.content, name=f'trip_image_{randint(1, 10000)}.jpg')








        self.stdout.write(self.style.SUCCESS('Data populated successfully.'))