from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import PriestProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates demo users for Punyaka MVP'

    def handle(self, *args, **options):
        # Create admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@punyaka.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create priests
        priests_data = [
            {
                'username': 'priest1',
                'email': 'priest1@punyaka.com',
                'password': 'priest123',
                'first_name': 'Ramesh',
                'last_name': 'Sharma',
                'phone': '+919876543210',
                'profile': {
                    'specializations': 'Vedic Rituals, Homas, Graha Shanti',
                    'experience_years': 15,
                    'languages': 'Hindi, Sanskrit, English',
                    'is_verified': True,
                    'average_rating': 4.8,
                    'total_ratings': 35,
                    'service_radius_km': 25,
                    'latitude': '19.0760',
                    'longitude': '72.8777',
                    'aadhaar_number': '123400000002',
                    'pan_number': 'ABCDE0002F',
                    'bank_account_number': '9876540000000002',
                    'bank_ifsc_code': 'SBIN0001234'
                }
            },
            {
                'username': 'priest2',
                'email': 'priest2@punyaka.com',
                'password': 'priest123',
                'first_name': 'Vijay',
                'last_name': 'Kumar',
                'phone': '+919876543211',
                'profile': {
                    'specializations': 'Poojas, Yagnas, Vastu Consultation',
                    'experience_years': 20,
                    'languages': 'Tamil, Sanskrit, English',
                    'is_verified': True,
                    'average_rating': 4.9,
                    'total_ratings': 42,
                    'service_radius_km': 30,
                    'latitude': '13.0827',
                    'longitude': '80.2707',
                    'aadhaar_number': '123400000003',
                    'pan_number': 'ABCDE0003F',
                    'bank_account_number': '9876540000000003',
                    'bank_ifsc_code': 'ICIC0001234'
                }
            },
            {
                'username': 'priest3',
                'email': 'priest3@punyaka.com',
                'password': 'priest123',
                'first_name': 'Mohan',
                'last_name': 'Patel',
                'phone': '+919876543212',
                'profile': {
                    'specializations': 'Havans, Weddings, Navagraha Pooja',
                    'experience_years': 12,
                    'languages': 'Hindi, Gujarati, English',
                    'is_verified': True,
                    'average_rating': 4.7,
                    'total_ratings': 28,
                    'service_radius_km': 20,
                    'latitude': '23.0225',
                    'longitude': '72.5714',
                    'aadhaar_number': '123400000004',
                    'pan_number': 'ABCDE0004F',
                    'bank_account_number': '9876540000000004',
                    'bank_ifsc_code': 'HDFC0001234'
                }
            }
        ]

        for data in priests_data:
            if not User.objects.filter(username=data['username']).exists():
                profile_data = data.pop('profile')
                user = User.objects.create_user(**data, role='priest')
                PriestProfile.objects.create(user=user, **profile_data)
                self.stdout.write(self.style.SUCCESS(f"Created priest: {data['username']}"))

        # Create customers
        customers_data = [
            {
                'username': 'customer1',
                'email': 'customer1@punyaka.com',
                'password': 'customer123',
                'first_name': 'Priya',
                'last_name': 'Mehta',
                'phone': '+919876543220',
                'date_of_birth': '1990-05-15',
                'time_of_birth': '10:30:00',
                'place_of_birth': 'Mumbai, India'
            },
            {
                'username': 'customer2',
                'email': 'customer2@punyaka.com',
                'password': 'customer123',
                'first_name': 'Rahul',
                'last_name': 'Singh',
                'phone': '+919876543221',
                'date_of_birth': '1985-08-22',
                'time_of_birth': '14:45:00',
                'place_of_birth': 'Delhi, India'
            },
            {
                'username': 'customer3',
                'email': 'customer3@punyaka.com',
                'password': 'customer123',
                'first_name': 'Anjali',
                'last_name': 'Verma',
                'phone': '+919876543222',
                'date_of_birth': '1992-11-30',
                'time_of_birth': '08:15:00',
                'place_of_birth': 'Bangalore, India'
            }
        ]

        for data in customers_data:
            if not User.objects.filter(username=data['username']).exists():
                User.objects.create_user(**data, role='customer')
                self.stdout.write(self.style.SUCCESS(f"Created customer: {data['username']}"))

        self.stdout.write(self.style.SUCCESS('✅ All demo users created successfully!'))
