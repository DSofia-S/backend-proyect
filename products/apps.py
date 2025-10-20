from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Configuración de la aplicación de productos.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    verbose_name = 'Productos del Catálogo'


