"""
Configuración ASGI para el proyecto de catálogo.

Expone el callable ASGI como una variable a nivel de módulo llamada ``application``.

Para más información sobre este archivo, consulta
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogo_backend.settings')

application = get_asgi_application()


