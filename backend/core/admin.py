from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PriestProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'date_of_birth', 'time_of_birth', 
                      'place_of_birth', 'address', 'profile_picture')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'email')
        }),
    )


@admin.register(PriestProfile)
class PriestProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified', 'experience_years', 'average_rating', 'verification_date']
    list_filter = ['is_verified', 'verification_date']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['average_rating', 'total_ratings', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Professional Info', {
            'fields': ('specializations', 'experience_years', 'languages', 'service_radius_km')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Verification Documents', {
            'fields': ('aadhaar_number', 'pan_number', 'bank_account_number', 'bank_ifsc_code')
        }),
        ('Verification Status', {
            'fields': ('is_verified', 'verification_date', 'verification_notes')
        }),
        ('Ratings', {
            'fields': ('average_rating', 'total_ratings')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['verify_priests', 'unverify_priests']
    
    def verify_priests(self, request, queryset):
        from django.utils import timezone
        count = queryset.update(is_verified=True, verification_date=timezone.now())
        self.message_user(request, f'{count} priest(s) verified successfully.')
    verify_priests.short_description = "Verify selected priests"
    
    def unverify_priests(self, request, queryset):
        count = queryset.update(is_verified=False, verification_date=None)
        self.message_user(request, f'{count} priest(s) unverified.')
    unverify_priests.short_description = "Unverify selected priests"
