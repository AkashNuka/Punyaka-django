#!/usr/bin/env python
"""
Script to initialize demo data on Render deployment.
Run this once after deployment to populate the database.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'punyaka.settings')
django.setup()

# Import management commands
from django.core.management import call_command

print("🚀 Initializing demo data...")

try:
    print("\n1️⃣ Creating demo users...")
    call_command('create_demo_users')
    
    print("\n2️⃣ Creating demo services and products...")
    call_command('create_demo_data')
    
    print("\n✅ Demo data initialization complete!")
    print("\n📝 Login credentials:")
    print("   Admin: admin@punyaka.com / admin123")
    print("   Priest 1: priest1@punyaka.com / priest123")
    print("   Priest 2: priest2@punyaka.com / priest123")
    print("   Priest 3: priest3@punyaka.com / priest123")
    print("   Customer 1: customer1@punyaka.com / customer123")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
