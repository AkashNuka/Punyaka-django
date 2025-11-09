# Generated migration for bookings app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('service_type', models.CharField(choices=[('pooja', 'Pooja'), ('homa', 'Homa'), ('vratam', 'Vratam'), ('other', 'Other')], max_length=50)),
                ('description', models.TextField()),
                ('duration_minutes', models.IntegerField(help_text='Estimated duration in minutes')),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('booking_time', models.TimeField()),
                ('location_address', models.TextField()),
                ('location_latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('location_longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('service_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('advance_payment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balance_payment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dakshina_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('partial', 'Partial (25%)'), ('full', 'Full Payment'), ('refunded', 'Refunded')], default='pending', max_length=20)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('completion_checklist', models.JSONField(blank=True, null=True)),
                ('customer_confirmed', models.BooleanField(default=False)),
                ('rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('special_instructions', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
                ('priest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='core.priestprofile')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bookings.service')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
