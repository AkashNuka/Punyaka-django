"""
Script to generate demo data fixture for Punyaka MVP
Run this to create demo_data.json
"""
import json
from datetime import datetime, timedelta, date, time
import random

# Helper to generate dates
today = date.today()
tomorrow = today + timedelta(days=1)
next_week = today + timedelta(days=7)

fixture = []
pk_counter = 1

# 1. Create Admin User
fixture.append({
    "model": "core.user",
    "pk": pk_counter,
    "fields": {
        "username": "admin",
        "password": "pbkdf2_sha256$720000$admin123$adminhashedpassword",  # password: admin123
        "email": "admin@punyaka.com",
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin",
        "is_staff": True,
        "is_superuser": True,
        "is_active": True,
        "date_joined": "2024-01-01T00:00:00Z"
    }
})
admin_pk = pk_counter
pk_counter += 1

# 2. Create Priest Users
priests_data = [
    {"username": "priest1", "email": "priest1@punyaka.com", "first_name": "Ramesh", "last_name": "Sharma", 
     "phone": "+919876543210", "specializations": "Vedic Rituals, Homas, Graha Shanti", 
     "experience": 15, "languages": "Hindi, Sanskrit, English", "rating": 4.8},
    {"username": "priest2", "email": "priest2@punyaka.com", "first_name": "Venkatesh", "last_name": "Iyer", 
     "phone": "+919876543211", "specializations": "Wedding Ceremonies, Satyanarayan Pooja, Vastu Shanti", 
     "experience": 10, "languages": "Tamil, Telugu, English", "rating": 4.6},
    {"username": "priest3", "email": "priest3@punyaka.com", "first_name": "Anand", "last_name": "Joshi", 
     "phone": "+919876543212", "specializations": "Ayush Homa, Navagraha Pooja, Rudra Abhishek", 
     "experience": 12, "languages": "Marathi, Hindi, English", "rating": 4.9},
]

priest_pks = []
for priest in priests_data:
    fixture.append({
        "model": "core.user",
        "pk": pk_counter,
        "fields": {
            "username": priest["username"],
            "password": "pbkdf2_sha256$720000$priest123$priesthashedpassword",  # password: priest123
            "email": priest["email"],
            "first_name": priest["first_name"],
            "last_name": priest["last_name"],
            "role": "priest",
            "phone": priest["phone"],
            "is_active": True,
            "date_joined": "2024-01-15T00:00:00Z"
        }
    })
    priest_user_pk = pk_counter
    priest_pks.append(pk_counter)
    pk_counter += 1
    
    # Create Priest Profile
    fixture.append({
        "model": "core.priestprofile",
        "pk": pk_counter,
        "fields": {
            "user": priest_user_pk,
            "specializations": priest["specializations"],
            "experience_years": priest["experience"],
            "languages": priest["languages"],
            "aadhaar_number": f"1234{pk_counter:08d}",
            "pan_number": f"ABCDE{pk_counter:04d}F",
            "bank_account_number": f"987654{pk_counter:010d}",
            "bank_ifsc_code": "SBIN0001234",
            "is_verified": True,
            "verification_date": "2024-02-01T00:00:00Z",
            "average_rating": priest["rating"],
            "total_ratings": random.randint(20, 50),
            "service_radius_km": 25,
            "latitude": "19.0760",
            "longitude": "72.8777"
        }
    })
    pk_counter += 1

# 3. Create Customer Users
customers_data = [
    {"username": "customer1", "email": "customer1@punyaka.com", "first_name": "Priya", "last_name": "Mehta", "phone": "+919876543220"},
    {"username": "customer2", "email": "customer2@punyaka.com", "first_name": "Raj", "last_name": "Kumar", "phone": "+919876543221"},
    {"username": "customer3", "email": "customer3@punyaka.com", "first_name": "Sneha", "last_name": "Patel", "phone": "+919876543222"},
]

customer_pks = []
for customer in customers_data:
    fixture.append({
        "model": "core.user",
        "pk": pk_counter,
        "fields": {
            "username": customer["username"],
            "password": "pbkdf2_sha256$720000$customer123$customerhashedpassword",  # password: customer123
            "email": customer["email"],
            "first_name": customer["first_name"],
            "last_name": customer["last_name"],
            "role": "customer",
            "phone": customer["phone"],
            "date_of_birth": "1990-05-15",
            "time_of_birth": "10:30:00",
            "place_of_birth": "Mumbai, India",
            "is_active": True,
            "date_joined": "2024-03-01T00:00:00Z"
        }
    })
    customer_pks.append(pk_counter)
    pk_counter += 1

# 4. Create Services
services_data = [
    {"name": "Satyanarayan Pooja", "type": "pooja", "duration": 180, "price": "2500.00", 
     "desc": "Traditional Satyanarayan Pooja for family well-being and prosperity"},
    {"name": "Graha Shanti Homa", "type": "homa", "duration": 240, "price": "5000.00", 
     "desc": "Planetary peace ritual to reduce malefic effects of planets"},
    {"name": "Navagraha Pooja", "type": "pooja", "duration": 120, "price": "1800.00", 
     "desc": "Worship of nine celestial deities for harmony and balance"},
    {"name": "Rudra Abhishek", "type": "pooja", "duration": 150, "price": "3000.00", 
     "desc": "Sacred bathing ritual of Lord Shiva for blessings and peace"},
    {"name": "Ayush Homa", "type": "homa", "duration": 180, "price": "4000.00", 
     "desc": "Fire ritual for longevity and good health"},
    {"name": "Vastu Shanti Pooja", "type": "pooja", "duration": 120, "price": "2200.00", 
     "desc": "Ritual for home harmony and positive energy"},
]

service_pks = []
for service in services_data:
    fixture.append({
        "model": "bookings.service",
        "pk": pk_counter,
        "fields": {
            "name": service["name"],
            "service_type": service["type"],
            "description": service["desc"],
            "duration_minutes": service["duration"],
            "base_price": service["price"],
            "is_active": True
        }
    })
    service_pks.append(pk_counter)
    pk_counter += 1

# 5. Create some Bookings
bookings_data = [
    {"customer": customer_pks[0], "priest": 2, "service": service_pks[0], "status": "confirmed", 
     "payment": "partial", "date": str(next_week), "time": "09:00:00"},
    {"customer": customer_pks[1], "priest": 3, "service": service_pks[1], "status": "completed", 
     "payment": "full", "date": str(today - timedelta(days=5)), "time": "10:00:00"},
    {"customer": customer_pks[2], "priest": 4, "service": service_pks[2], "status": "pending", 
     "payment": "pending", "date": str(tomorrow), "time": "11:00:00"},
]

for booking in bookings_data:
    fixture.append({
        "model": "bookings.booking",
        "pk": pk_counter,
        "fields": {
            "customer": booking["customer"],
            "priest": booking["priest"],
            "service": booking["service"],
            "booking_date": booking["date"],
            "booking_time": booking["time"],
            "location_address": "123, Sample Street, Mumbai, Maharashtra - 400001",
            "location_latitude": "19.0760",
            "location_longitude": "72.8777",
            "service_price": "2500.00",
            "advance_payment": "625.00",
            "balance_payment": "1875.00",
            "dakshina_amount": "0.00",
            "status": booking["status"],
            "payment_status": booking["payment"],
            "special_instructions": "Please bring necessary samagri",
            "created_at": f"{today}T00:00:00Z"
        }
    })
    pk_counter += 1

# 6. Create Categories
categories_data = [
    {"name": "Pooja Samagri", "slug": "pooja-samagri", "desc": "Essential items for Hindu rituals"},
    {"name": "Incense & Dhoop", "slug": "incense-dhoop", "desc": "Fragrant offerings for worship"},
    {"name": "Idols & Murtis", "slug": "idols-murtis", "desc": "Sacred deity statues"},
    {"name": "Prasad Items", "slug": "prasad-items", "desc": "Blessed food offerings"},
    {"name": "Gift Items", "slug": "gift-items", "desc": "Spiritual gifts for loved ones"},
]

category_pks = []
for category in categories_data:
    fixture.append({
        "model": "ecommerce.category",
        "pk": pk_counter,
        "fields": {
            "name": category["name"],
            "slug": category["slug"],
            "description": category["desc"]
        }
    })
    category_pks.append(pk_counter)
    pk_counter += 1

# 7. Create Products
products_data = [
    {"name": "Complete Pooja Kit", "slug": "complete-pooja-kit", "type": "kit", "category": category_pks[0], 
     "price": "599.00", "discount": "499.00", "stock": 50, "featured": True,
     "desc": "Complete pooja essentials including kumkum, haldi, agarbatti, camphor, and more"},
    {"name": "Navagraha Pooja Kit", "slug": "navagraha-pooja-kit", "type": "samagri", "category": category_pks[0], 
     "price": "799.00", "discount": None, "stock": 30, "featured": True,
     "desc": "Special kit for Navagraha worship with specific items for each planet"},
    {"name": "Premium Agarbatti Set", "slug": "premium-agarbatti-set", "type": "samagri", "category": category_pks[1], 
     "price": "299.00", "discount": "249.00", "stock": 100, "featured": False,
     "desc": "Assorted pack of fragrant incense sticks - Rose, Sandalwood, Jasmine"},
    {"name": "Brass Diya Set (5 pcs)", "slug": "brass-diya-set", "type": "samagri", "category": category_pks[0], 
     "price": "450.00", "discount": None, "stock": 40, "featured": False,
     "desc": "Handcrafted brass diyas for lighting during pooja"},
    {"name": "Ganesha Idol (Small)", "slug": "ganesha-idol-small", "type": "gift", "category": category_pks[2], 
     "price": "399.00", "discount": "349.00", "stock": 25, "featured": True,
     "desc": "Beautiful brass Ganesha idol - 4 inches height"},
    {"name": "Lakshmi Idol (Medium)", "slug": "lakshmi-idol-medium", "type": "gift", "category": category_pks[2], 
     "price": "899.00", "discount": None, "stock": 15, "featured": False,
     "desc": "Elegant brass Lakshmi idol - 6 inches height"},
    {"name": "Kumkum & Haldi Pack", "slug": "kumkum-haldi-pack", "type": "samagri", "category": category_pks[0], 
     "price": "149.00", "discount": "129.00", "stock": 80, "featured": False,
     "desc": "Pure kumkum and haldi powder - 100g each"},
    {"name": "Camphor Tablets (Pack of 25)", "slug": "camphor-tablets", "type": "samagri", "category": category_pks[0], 
     "price": "99.00", "discount": None, "stock": 150, "featured": False,
     "desc": "Pure camphor tablets for aarti"},
    {"name": "Rudraksha Mala", "slug": "rudraksha-mala", "type": "gift", "category": category_pks[4], 
     "price": "699.00", "discount": "599.00", "stock": 20, "featured": True,
     "desc": "108 beads Rudraksha mala for meditation and prayer"},
    {"name": "Silver Plated Pooja Thali", "slug": "silver-pooja-thali", "type": "gift", "category": category_pks[0], 
     "price": "1299.00", "discount": "1099.00", "stock": 12, "featured": True,
     "desc": "Decorative silver plated thali set for pooja"},
]

for product in products_data:
    fixture.append({
        "model": "ecommerce.product",
        "pk": pk_counter,
        "fields": {
            "name": product["name"],
            "slug": product["slug"],
            "description": product["desc"],
            "product_type": product["type"],
            "category": product["category"],
            "price": product["price"],
            "discount_price": product["discount"],
            "stock": product["stock"],
            "is_in_stock": True,
            "gift_wrap_available": product["type"] == "gift",
            "gift_wrap_price": "50.00" if product["type"] == "gift" else "0.00",
            "is_active": True,
            "is_featured": product["featured"]
        }
    })
    pk_counter += 1

# Write to file
output_file = "demo_data.json"
with open(output_file, 'w') as f:
    json.dump(fixture, f, indent=2)

print(f"Demo data fixture created: {output_file}")
print(f"Total objects: {len(fixture)}")
print(f"\n Demo Credentials:")
print(f"Admin: admin@punyaka.com / admin123")
print(f"Priest: priest1@punyaka.com / priest123")
print(f"Customer: customer1@punyaka.com / customer123")
