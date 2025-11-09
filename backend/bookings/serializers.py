from rest_framework import serializers
from .models import Service, Booking
from core.serializers import UserSerializer, PriestProfileSerializer


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    customer_details = UserSerializer(source='customer', read_only=True)
    priest_details = PriestProfileSerializer(source='priest', read_only=True)
    service_details = ServiceSerializer(source='service', read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['advance_payment', 'balance_payment', 'created_at', 'updated_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['priest', 'service', 'booking_date', 'booking_time', 
                 'location_address', 'location_latitude', 'location_longitude',
                 'service_price', 'special_instructions']
    
    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        return super().create(validated_data)
