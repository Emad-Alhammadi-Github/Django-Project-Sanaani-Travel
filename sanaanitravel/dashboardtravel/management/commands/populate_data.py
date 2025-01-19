from django.core.management.base import BaseCommand
from dashboardtravel.models import Nationality, City, TravelType, TripCategory,Employee
from django.contrib.auth.models import User
class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **kwargs):
        nationalities = [
            'اليمن', 'مصر', 'السعودية', 'الأردن', 'العراق',
            'فلسطين', 'سوريا', 'لبنان', 'الإمارات', 'الكويت',
        ]

        for country in nationalities:
            Nationality.objects.get_or_create(name=country)

        yemen_nationality = Nationality.objects.get(name='اليمن')
        cities = [
        'صنعاء', 'عدن', 'المكلا', 'تعز', 'الحديدة',
        'البيضاء', 'إب', 'لحج', 'مأرب', 'صعدة',
 
        ]

        for city in cities:
          City.objects.get_or_create(name=city, nationality=yemen_nationality)

        travel_types = [
            'برّي', 'بحري',
        ]

        for travel_type in travel_types:
            TravelType.objects.get_or_create(name=travel_type)

        trip_categories = [
            'الشاحنات', 'خاصة', 'عامة','الداخلية','الخارجية'
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

        self.stdout.write(self.style.SUCCESS('Data populated successfully.'))