"""
ASGI config for punyaka project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'punyaka.settings')

application = get_asgi_application()
