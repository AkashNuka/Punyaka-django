from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register_view, login_view, logout_view, current_user_view, csrf_token_view,
    PriestProfileViewSet
)

router = DefaultRouter()
router.register(r'priests', PriestProfileViewSet, basename='priest')

urlpatterns = [
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/me/', current_user_view, name='current-user'),
    path('auth/csrf/', csrf_token_view, name='csrf-token'),
    path('', include(router.urls)),
]
