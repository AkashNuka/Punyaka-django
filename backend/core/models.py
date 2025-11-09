from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with role-based authentication"""
    
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('priest', 'Priest'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    time_of_birth = models.TimeField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        ordering = ['-created_at']


class PriestProfile(models.Model):
    """Extended profile for priests with verification"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='priest_profile')
    specializations = models.TextField(help_text="Comma-separated specializations")
    experience_years = models.IntegerField(default=0)
    languages = models.CharField(max_length=255, help_text="Comma-separated languages")
    
    # Verification documents
    aadhaar_number = models.CharField(max_length=12, blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    bank_account_number = models.CharField(max_length=20, blank=True, null=True)
    bank_ifsc_code = models.CharField(max_length=11, blank=True, null=True)
    
    # Verification status
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(blank=True, null=True)
    verification_notes = models.TextField(blank=True, null=True)
    
    # Ratings
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_ratings = models.IntegerField(default=0)
    
    # Service area
    service_radius_km = models.IntegerField(default=25, help_text="Service radius in kilometers")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {'Verified' if self.is_verified else 'Unverified'}"
    
    class Meta:
        ordering = ['-average_rating', '-created_at']
