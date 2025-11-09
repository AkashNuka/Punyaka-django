from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.middleware.csrf import get_token
from .models import User, PriestProfile
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, PriestProfileSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Register a new user"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        # Ensure CSRF token is set
        get_token(request)
        response = Response({
            'user': UserSerializer(user).data,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)
        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login user"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        # Ensure CSRF token is set
        get_token(request)
        response = Response({
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        })
        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout user"""
    logout(request)
    return Response({'message': 'Logout successful'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """Get current logged-in user"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_token_view(request):
    """Get CSRF token"""
    return Response({'csrfToken': get_token(request)})


class PriestProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing priest profiles
    Only verified priests are shown to public
    """
    serializer_class = PriestProfileSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = PriestProfile.objects.filter(is_verified=True)
        
        # Filter by specialization
        specialization = self.request.query_params.get('specialization', None)
        if specialization:
            queryset = queryset.filter(specializations__icontains=specialization)
        
        # Filter by minimum rating
        min_rating = self.request.query_params.get('min_rating', None)
        if min_rating:
            queryset = queryset.filter(average_rating__gte=float(min_rating))
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get priest's availability (placeholder for future slot integration)"""
        priest = self.get_object()
        return Response({
            'priest_id': priest.id,
            'message': 'Availability checking not yet implemented'
        })
