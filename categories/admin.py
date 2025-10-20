"""
Configuración del panel de administración para categorías.
"""
from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Category.
    """
    
    # Campos a mostrar en la lista
    list_display = [
        'name', 
        'description', 
        'is_active', 
        'created_at',
        'get_products_count'
    ]
    
    # Campos por los que se puede filtrar
    list_filter = [
        'is_active',
        'created_at',
        'updated_at'
    ]
    
    # Campos por los que se puede buscar
    search_fields = [
        'name',
        'description'
    ]
    
    # Campos de solo lectura
    readonly_fields = [
        'created_at',
        'updated_at'
    ]
    
    # Ordenamiento por defecto
    ordering = ['name']
    
    # Campos editables en la lista
    list_editable = ['is_active']
    
    # Campos agrupados en el formulario
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'description')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_products_count(self, obj):
        """
        Muestra el número de productos en la categoría.
        """
        return obj.get_products_count()
    get_products_count.short_description = 'Número de productos'
    get_products_count.admin_order_field = 'products__count'


