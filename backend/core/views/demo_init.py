from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def initialize_demo_data(request):
    """
    Initialize demo data. Can only be called once or when no data exists.
    """
    from core.models import User
    from bookings.models import Service
    from ecommerce.models import Product
    
    # Check if data already exists
    user_count = User.objects.count()
    service_count = Service.objects.count()
    product_count = Product.objects.count()
    
    if user_count > 0 or service_count > 0 or product_count > 0:
        return JsonResponse({
            'status': 'skipped',
            'message': 'Demo data already exists',
            'users': user_count,
            'services': service_count,
            'products': product_count
        })
    
    try:
        # Create demo users
        call_command('create_demo_users')
        logger.info("Demo users created successfully")
        
        # Create demo data
        call_command('create_demo_data')
        logger.info("Demo data created successfully")
        
        # Get counts
        user_count = User.objects.count()
        service_count = Service.objects.count()
        product_count = Product.objects.count()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Demo data initialized successfully',
            'users': user_count,
            'services': service_count,
            'products': product_count
        })
    except Exception as e:
        logger.error(f"Error initializing demo data: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
