from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, PriestProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                 'phone', 'date_of_birth', 'time_of_birth', 'place_of_birth', 
                 'address', 'profile_picture', 'created_at']
        read_only_fields = ['id', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 
                 'last_name', 'role', 'phone', 'date_of_birth', 'time_of_birth', 
                 'place_of_birth']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        
        # Create priest profile if role is priest
        if user.role == 'priest':
            PriestProfile.objects.create(user=user)
        
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        # Try to authenticate with username first
        user = authenticate(username=username, password=password)
        
        # If failed, try with email
        if not user:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Invalid credentials")


class PriestProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    specializations_list = serializers.SerializerMethodField()
    languages_list = serializers.SerializerMethodField()
    
    class Meta:
        model = PriestProfile
        fields = '__all__'
        read_only_fields = ['average_rating', 'total_ratings', 'is_verified', 
                           'verification_date', 'created_at', 'updated_at']
    
    def get_specializations_list(self, obj):
        return [s.strip() for s in obj.specializations.split(',')] if obj.specializations else []
    
    def get_languages_list(self, obj):
        return [l.strip() for l in obj.languages.split(',')] if obj.languages else []
