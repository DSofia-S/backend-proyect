from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    """
    Configuración de la aplicación de categorías.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'categories'
    verbose_name = 'Categorías de Productos'


