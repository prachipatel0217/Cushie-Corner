#!/usr/bin/env python
"""
Cushie Corner - Database Setup Script
Run this after installing Django to set up your database and create sample products.

Usage:
    python setup.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cushie_corner.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.core.management import call_command

print("=== Cushie Corner Setup ===\n")

print("1. Running migrations...")
call_command('migrate', verbosity=1)

print("\n2. Creating sample products...")
from store.models import Product

products = [
    {"name": "Mini Cushion - Black Leather", "description": "Elegant black leather mini cushion, perfect for jewelry display", "price": 499, "image_filename": "cushion1.jpg", "stock": 15},
    {"name": "Royal Blue Cushion", "description": "Vibrant blue cushion, ideal for rings and necklaces", "price": 699, "image_filename": "cushion2.jpg", "stock": 12},
    {"name": "Floral Navy Cushion", "description": "Hand-painted daisy pattern on deep navy blue", "price": 799, "image_filename": "cushion3.jpg", "stock": 10},
    {"name": "Heart Print Cushion", "description": "Romantic pink cushion with red heart motifs", "price": 599, "image_filename": "cushion4.jpg", "stock": 20},
    {"name": "Shell Tray - Ocean Blue", "description": "Beautiful ocean-inspired shell shaped tray", "price": 899, "image_filename": "cushion5.jpg", "stock": 8},
    {"name": "Pearl Shell Tray", "description": "Elegant cream ceramic shell tray with candles", "price": 999, "image_filename": "cushion6.jpg", "stock": 6},
]

created_count = 0
for p in products:
    obj, created = Product.objects.get_or_create(name=p["name"], defaults=p)
    if created:
        created_count += 1
        print(f"   ✓ Created: {p['name']} - ₹{p['price']}")

if created_count == 0:
    print("   (Products already exist)")

print(f"\n3. Creating superuser for admin panel...")
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@cushiecorner.in', 'admin123')
    print("   ✓ Admin user created: username=admin, password=admin123")
else:
    print("   (Admin user already exists)")

print("\n=== Setup Complete! ===")
print("\nTo run the server:")
print("   python manage.py runserver")
print("\nAdmin panel: http://127.0.0.1:8000/admin/")
print("   Username: admin | Password: admin123")
print("\nWebsite: http://127.0.0.1:8000/")
print("\nNOTE: Place your cushion images in: store/static/store/images/")
