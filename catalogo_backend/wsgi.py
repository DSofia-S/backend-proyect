"""
Configuración WSGI para el proyecto de catálogo.

Expone el callable WSGI como una variable a nivel de módulo llamada ``application``.

Para más información sobre este archivo, consulta
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogo_backend.settings')

application = get_wsgi_application()


