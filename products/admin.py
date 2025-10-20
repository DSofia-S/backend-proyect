"""
Configuración del panel de administración para productos.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """
    Inline para gestionar imágenes adicionales de productos.
    """
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Product.
    """
    
    # Campos a mostrar en la lista
    list_display = [
        'name',
        'category',
        'price_display',
        'stock',
        'is_in_stock_display',
        'is_active',
        'created_at'
    ]
    
    # Campos por los que se puede filtrar
    list_filter = [
        'category',
        'is_active',
        'created_at',
        'updated_at'
    ]
    
    # Campos por los que se puede buscar
    search_fields = [
        'name',
        'description',
        'sku'
    ]
    
    # Campos de solo lectura
    readonly_fields = [
        'sku',
        'created_at',
        'updated_at'
    ]
    
    # Ordenamiento por defecto
    ordering = ['-created_at']
    
    # Campos editables en la lista
    list_editable = ['is_active']
    
    # Campos agrupados en el formulario
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'description', 'sku')
        }),
        ('Precio y categoría', {
            'fields': ('price', 'category')
        }),
        ('Inventario', {
            'fields': ('stock', 'is_active')
        }),
        ('Imagen principal', {
            'fields': ('image',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Inlines
    inlines = [ProductImageInline]
    
    # Acciones personalizadas
    actions = ['activate_products', 'deactivate_products', 'update_stock']
    
    def price_display(self, obj):
        """
        Muestra el precio formateado como moneda.
        """
        return obj.get_price_display()
    price_display.short_description = 'Precio'
    price_display.admin_order_field = 'price'
    
    def is_in_stock_display(self, obj):
        """
        Muestra si el producto está en stock con un indicador visual.
        """
        if obj.is_in_stock():
            return format_html(
                '<span style="color: green;">✓ En stock</span>'
            )
        else:
            return format_html(
                '<span style="color: red;">✗ Sin stock</span>'
            )
    is_in_stock_display.short_description = 'Stock'
    
    def activate_products(self, request, queryset):
        """
        Activa los productos seleccionados.
        """
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} productos fueron activados correctamente.'
        )
    activate_products.short_description = 'Activar productos seleccionados'
    
    def deactivate_products(self, request, queryset):
        """
        Desactiva los productos seleccionados.
        """
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} productos fueron desactivados correctamente.'
        )
    deactivate_products.short_description = 'Desactivar productos seleccionados'
    
    def update_stock(self, request, queryset):
        """
        Actualiza el stock de los productos seleccionados.
        """
        # Esta es una acción de ejemplo, en un caso real podrías
        # redirigir a una página de formulario para actualizar el stock
        self.message_user(
            request,
            'Función de actualización de stock en desarrollo.'
        )
    update_stock.short_description = 'Actualizar stock de productos seleccionados'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo ProductImage.
    """
    
    list_display = [
        'product',
        'image_preview',
        'alt_text',
        'is_primary',
        'created_at'
    ]
    
    list_filter = [
        'is_primary',
        'created_at'
    ]
    
    search_fields = [
        'product__name',
        'alt_text'
    ]
    
    readonly_fields = ['created_at']
    
    def image_preview(self, obj):
        """
        Muestra una vista previa de la imagen.
        """
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
                obj.image.url
            )
        return "Sin imagen"
    image_preview.short_description = 'Vista previa'



