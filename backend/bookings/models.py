from django.db import models
from core.models import User, PriestProfile


class Service(models.Model):
    """Services offered by priests"""
    
    SERVICE_TYPES = (
        ('pooja', 'Pooja'),
        ('homa', 'Homa'),
        ('vratam', 'Vratam'),
        ('other', 'Other'),
    )
    
    name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    description = models.TextField()
    duration_minutes = models.IntegerField(help_text="Estimated duration in minutes")
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"
    
    class Meta:
        ordering = ['name']


class Booking(models.Model):
    """Priest booking for physical services"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('partial', 'Partial (25%)'),
        ('full', 'Full Payment'),
        ('refunded', 'Refunded'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    priest = models.ForeignKey(PriestProfile, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    
    # Booking details
    booking_date = models.DateField()
    booking_time = models.TimeField()
    location_address = models.TextField()
    location_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Pricing
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2)  # 25%
    balance_payment = models.DecimalField(max_digits=10, decimal_places=2)  # 75%
    dakshina_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Completion details
    completed_at = models.DateTimeField(blank=True, null=True)
    completion_checklist = models.JSONField(blank=True, null=True)
    customer_confirmed = models.BooleanField(default=False)
    
    # Rating and feedback
    rating = models.IntegerField(blank=True, null=True, choices=[(i, i) for i in range(1, 6)])
    feedback = models.TextField(blank=True, null=True)
    
    # Special instructions
    special_instructions = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking #{self.id} - {self.customer.username} with {self.priest.user.get_full_name()}"
    
    def save(self, *args, **kwargs):
        # Calculate advance and balance if not set
        if not self.advance_payment and not self.balance_payment:
            self.advance_payment = self.service_price * 0.25
            self.balance_payment = self.service_price * 0.75
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']
