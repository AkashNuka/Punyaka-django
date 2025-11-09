from django.core.management.base import BaseCommand
from bookings.models import Service
from ecommerce.models import Category, Product


class Command(BaseCommand):
    help = 'Creates demo services and products for Punyaka MVP'

    def handle(self, *args, **options):
        # Create Services
        services_data = [
            {
                'name': 'Graha Shanti Pooja',
                'service_type': 'pooja',
                'description': 'Complete planetary peace ritual for removing negative influences of planets. Includes homa, mantra chanting, and offerings to all nine planets.',
                'duration_minutes': 180,
                'base_price': 5100.00
            },
            {
                'name': 'Ganesh Chaturthi Pooja',
                'service_type': 'pooja',
                'description': 'Traditional Ganesh Chaturthi celebration with full rituals, modak offering, and aarti.',
                'duration_minutes': 120,
                'base_price': 2500.00
            },
            {
                'name': 'Satyanarayan Katha',
                'service_type': 'pooja',
                'description': 'Complete Satyanarayan puja with katha recitation, prasad preparation, and family blessings.',
                'duration_minutes': 120,
                'base_price': 3100.00
            },
            {
                'name': 'House Warming Ceremony (Griha Pravesh)',
                'service_type': 'homa',
                'description': 'Complete house warming rituals for new home entry. Includes Vastu pooja, Ganesh pooja, and homa.',
                'duration_minutes': 240,
                'base_price': 7500.00
            },
            {
                'name': 'Rudrabhishek',
                'service_type': 'pooja',
                'description': 'Complete Shiva abhishekam with Rudra mantras, panchamrit, and sacred offerings.',
                'duration_minutes': 120,
                'base_price': 4200.00
            },
            {
                'name': 'Lakshmi Pooja',
                'service_type': 'pooja',
                'description': 'Goddess Lakshmi worship for prosperity and wealth. Perfect for Diwali or new business ventures.',
                'duration_minutes': 120,
                'base_price': 2800.00
            }
        ]

        for data in services_data:
            Service.objects.get_or_create(name=data['name'], defaults=data)
        
        self.stdout.write(self.style.SUCCESS(f'✅ Created {len(services_data)} services'))

        # Create Categories
        categories_data = [
            {'name': 'Pooja Items', 'slug': 'pooja-items', 'description': 'Essential items for daily worship and rituals'},
            {'name': 'Spiritual Books', 'slug': 'spiritual-books', 'description': 'Sacred texts and spiritual literature'},
            {'name': 'Idols & Yantras', 'slug': 'idols-yantras', 'description': 'Divine idols and sacred geometric diagrams'}
        ]

        created_categories = {}
        for data in categories_data:
            category, _ = Category.objects.get_or_create(slug=data['slug'], defaults=data)
            created_categories[data['slug']] = category
        
        self.stdout.write(self.style.SUCCESS(f'✅ Created {len(categories_data)} categories'))

        # Create Products
        products_data = [
            {
                'name': 'Brass Diya Set (6 pieces)',
                'slug': 'brass-diya-set-6',
                'description': 'Handcrafted brass diyas perfect for daily pooja and festivals. Each diya is 3 inches in diameter.',
                'category': created_categories['pooja-items'],
                'price': 850.00,
                'stock': 50
            },
            {
                'name': 'Bhagavad Gita (Sanskrit-English)',
                'slug': 'bhagavad-gita-sanskrit-english',
                'description': 'Complete Bhagavad Gita with Sanskrit shlokas and English translation. Hardcover edition with commentary.',
                'category': created_categories['spiritual-books'],
                'price': 450.00,
                'stock': 100
            },
            {
                'name': 'Ganesh Brass Idol (8 inches)',
                'slug': 'ganesh-brass-idol-8',
                'description': 'Beautiful brass Ganesh idol with fine detailing. Perfect for home temple or office.',
                'category': created_categories['idols-yantras'],
                'price': 2500.00,
                'stock': 25
            },
            {
                'name': 'Incense Sticks Combo Pack',
                'slug': 'incense-sticks-combo',
                'description': 'Premium agarbatti combo with 5 fragrances - Sandalwood, Rose, Jasmine, Mogra, Lavender. 100 sticks per box.',
                'category': created_categories['pooja-items'],
                'price': 350.00,
                'stock': 200
            },
            {
                'name': 'Sri Yantra (Brass)',
                'slug': 'sri-yantra-brass',
                'description': 'Authentic Sri Yantra made of brass. 6 inch diameter sacred geometric design for prosperity.',
                'category': created_categories['idols-yantras'],
                'price': 1800.00,
                'stock': 30
            },
            {
                'name': 'Rudraksha Mala (108 beads)',
                'slug': 'rudraksha-mala-108',
                'description': 'Genuine 5 Mukhi Rudraksha mala with 108+1 beads. Perfect for meditation and japa.',
                'category': created_categories['pooja-items'],
                'price': 1500.00,
                'stock': 75
            },
            {
                'name': 'Hanuman Chalisa Book',
                'slug': 'hanuman-chalisa-book',
                'description': 'Pocket-sized Hanuman Chalisa with Hindi and English transliteration. Includes meaning and benefits.',
                'category': created_categories['spiritual-books'],
                'price': 150.00,
                'stock': 150
            },
            {
                'name': 'Pooja Thali Set (Brass)',
                'slug': 'pooja-thali-set-brass',
                'description': 'Complete brass pooja thali set with 7 items - plate, diya, bell, incense holder, kumkum box, water pot.',
                'category': created_categories['pooja-items'],
                'price': 2200.00,
                'stock': 40
            },
            {
                'name': 'Lakshmi-Ganesh Idol Pair',
                'slug': 'lakshmi-ganesh-idol-pair',
                'description': 'Beautiful brass idol pair of Goddess Lakshmi and Lord Ganesh. 6 inches height each.',
                'category': created_categories['idols-yantras'],
                'price': 3500.00,
                'stock': 20
            },
            {
                'name': 'Camphor Tablets (Pure)',
                'slug': 'camphor-tablets-pure',
                'description': '100% pure camphor tablets for aarti and spiritual purposes. Pack of 50 tablets.',
                'category': created_categories['pooja-items'],
                'price': 180.00,
                'stock': 300
            }
        ]

        for data in products_data:
            Product.objects.get_or_create(slug=data['slug'], defaults=data)
        
        self.stdout.write(self.style.SUCCESS(f'✅ Created {len(products_data)} products'))
        self.stdout.write(self.style.SUCCESS('🎉 All demo data created successfully!'))
