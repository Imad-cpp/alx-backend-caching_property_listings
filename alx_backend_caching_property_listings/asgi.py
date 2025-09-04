import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_caching_property_listings.settings')

application = get_asgi_application()