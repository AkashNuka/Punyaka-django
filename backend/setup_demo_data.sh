#!/bin/bash
# Setup script to run after migrations

echo "Creating demo users..."
python manage.py create_demo_users

echo "Creating demo data..."
python manage.py create_demo_data

echo "Demo data setup complete!"
