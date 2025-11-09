from django.contrib import admin
from .models import Service, Booking


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'base_price', 'duration_minutes', 'is_active']
    list_filter = ['service_type', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'priest', 'service', 'booking_date', 
                   'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'booking_date']
    search_fields = ['customer__username', 'priest__user__username', 'service__name']
    readonly_fields = ['created_at', 'updated_at', 'advance_payment', 'balance_payment']
    
    fieldsets = (
        ('Booking Info', {
            'fields': ('customer', 'priest', 'service', 'booking_date', 'booking_time')
        }),
        ('Location', {
            'fields': ('location_address', 'location_latitude', 'location_longitude')
        }),
        ('Pricing', {
            'fields': ('service_price', 'advance_payment', 'balance_payment', 'dakshina_amount')
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Completion', {
            'fields': ('completed_at', 'completion_checklist', 'customer_confirmed')
        }),
        ('Feedback', {
            'fields': ('rating', 'feedback')
        }),
        ('Additional', {
            'fields': ('special_instructions', 'created_at', 'updated_at')
        }),
    )
