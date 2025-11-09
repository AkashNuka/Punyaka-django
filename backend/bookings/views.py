from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from .models import Service, Booking
from .serializers import ServiceSerializer, BookingSerializer, BookingCreateSerializer


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing services"""
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        service_type = self.request.query_params.get('type', None)
        if service_type:
            queryset = queryset.filter(service_type=service_type)
        return queryset


class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing bookings"""
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Booking.objects.filter(customer=user)
        elif user.role == 'priest':
            return Booking.objects.filter(priest__user=user)
        elif user.role == 'admin':
            return Booking.objects.all()
        return Booking.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Priest confirms booking"""
        booking = self.get_object()
        if request.user.role != 'priest':
            return Response({'error': 'Only priests can confirm bookings'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        booking.status = 'confirmed'
        booking.payment_status = 'partial'
        booking.save()
        
        return Response({
            'message': 'Booking confirmed',
            'booking': BookingSerializer(booking).data
        })
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Priest marks booking as completed"""
        booking = self.get_object()
        if request.user.role != 'priest':
            return Response({'error': 'Only priests can complete bookings'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        booking.status = 'completed'
        booking.completed_at = timezone.now()
        booking.completion_checklist = request.data.get('checklist', {})
        booking.save()
        
        return Response({
            'message': 'Booking marked as completed. Waiting for customer confirmation.',
            'booking': BookingSerializer(booking).data
        })
    
    @action(detail=True, methods=['post'])
    def customer_confirm(self, request, pk=None):
        """Customer confirms service completion and triggers final payment"""
        booking = self.get_object()
        if booking.customer != request.user:
            return Response({'error': 'Unauthorized'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        booking.customer_confirmed = True
        booking.payment_status = 'full'
        booking.dakshina_amount = request.data.get('dakshina', 0)
        booking.save()
        
        return Response({
            'message': 'Service confirmed. Payment processed.',
            'booking': BookingSerializer(booking).data
        })
    
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        """Customer rates the service"""
        booking = self.get_object()
        if booking.customer != request.user:
            return Response({'error': 'Unauthorized'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        rating = request.data.get('rating')
        feedback = request.data.get('feedback', '')
        
        if not rating or rating < 1 or rating > 5:
            return Response({'error': 'Rating must be between 1 and 5'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        booking.rating = rating
        booking.feedback = feedback
        booking.save()
        
        # Update priest's average rating
        priest = booking.priest
        total_bookings = Booking.objects.filter(
            priest=priest, 
            rating__isnull=False
        ).count()
        avg_rating = Booking.objects.filter(
            priest=priest, 
            rating__isnull=False
        ).aggregate(models.Avg('rating'))['rating__avg']
        
        priest.average_rating = avg_rating or 0
        priest.total_ratings = total_bookings
        priest.save()
        
        return Response({
            'message': 'Thank you for your feedback!',
            'booking': BookingSerializer(booking).data
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        
        if booking.status in ['completed', 'cancelled']:
            return Response({'error': 'Cannot cancel this booking'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        booking.status = 'cancelled'
        booking.save()
        
        return Response({
            'message': 'Booking cancelled',
            'booking': BookingSerializer(booking).data
        })
