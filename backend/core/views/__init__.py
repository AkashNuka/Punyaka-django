# Views package
# Import everything from the main views module to maintain backward compatibility
from ..views_main import (
    register_view, 
    login_view, 
    logout_view, 
    current_user_view,
    csrf_token_view,
    PriestProfileViewSet
)

__all__ = [
    'register_view',
    'login_view',
    'logout_view',
    'current_user_view',
    'csrf_token_view',
    'PriestProfileViewSet',
]
