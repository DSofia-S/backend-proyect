"""
Modelos para la gestión de categorías de productos.
Basado en la estructura definida en el frontend React.
"""
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """
    Modelo para representar las categorías de productos.
    
    Atributos:
        name: Nombre de la categoría (único)
        description: Descripción opcional de la categoría
        created_at: Fecha de creación del registro
        updated_at: Fecha de última actualización
        is_active: Indica si la categoría está activa
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre de la categoría',
        help_text='Nombre único de la categoría'
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción',
        help_text='Descripción opcional de la categoría'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activa',
        help_text='Indica si la categoría está disponible'
    )

    class Meta:
        """
        Configuración de metadatos del modelo.
        """
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
        db_table = 'categories'

    def __str__(self):
        """
        Representación en string del objeto.
        """
        return self.name

    def get_products_count(self):
        """
        Retorna el número de productos en esta categoría.
        """
        return self.products.count()

    def soft_delete(self):
        """
        Eliminación lógica de la categoría.
        """
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])


