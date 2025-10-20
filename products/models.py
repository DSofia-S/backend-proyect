"""
Modelos para la gestión de productos del catálogo.
Basado en la estructura definida en el frontend React.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from categories.models import Category


class Product(models.Model):
    """
    Modelo para representar los productos del catálogo.
    
    Atributos:
        name: Nombre del producto
        description: Descripción detallada del producto
        price: Precio del producto (en centavos para evitar problemas de decimales)
        category: Categoría a la que pertenece el producto
        image: Imagen del producto (opcional)
        stock: Cantidad disponible en inventario
        sku: Código único del producto
        is_active: Indica si el producto está activo
        created_at: Fecha de creación del registro
        updated_at: Fecha de última actualización
    """
    
    name = models.CharField(
        max_length=200,
        verbose_name='Nombre del producto',
        help_text='Nombre descriptivo del producto'
    )
    
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción detallada del producto'
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Precio',
        help_text='Precio del producto en pesos colombianos'
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Categoría',
        help_text='Categoría a la que pertenece el producto'
    )
    
    image = models.ImageField(
        upload_to='products/images/',
        blank=True,
        null=True,
        verbose_name='Imagen',
        help_text='Imagen del producto (opcional)'
    )
    
    stock = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Stock',
        help_text='Cantidad disponible en inventario'
    )
    
    sku = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name='SKU',
        help_text='Código único del producto (se genera automáticamente si no se proporciona)'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Indica si el producto está disponible'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )

    class Meta:
        """
        Configuración de metadatos del modelo.
        """
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']
        db_table = 'products'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['price']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        """
        Representación en string del objeto.
        """
        return f"{self.name} - {self.category.name}"

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para generar SKU automáticamente.
        """
        if not self.sku:
            # Generar SKU basado en el nombre y la fecha
            import uuid
            name_slug = self.name.replace(' ', '').upper()[:10]
            date_slug = timezone.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:8].upper()
            self.sku = f"{name_slug}-{date_slug}-{unique_id}"
        
        super().save(*args, **kwargs)

    def get_price_display(self):
        """
        Retorna el precio formateado como moneda.
        """
        return f"${self.price:,.2f}"

    def is_in_stock(self):
        """
        Verifica si el producto tiene stock disponible.
        """
        return self.stock > 0

    def reduce_stock(self, quantity):
        """
        Reduce el stock del producto.
        
        Args:
            quantity: Cantidad a reducir
            
        Returns:
            bool: True si se pudo reducir el stock, False en caso contrario
        """
        if self.stock >= quantity:
            self.stock -= quantity
            self.save(update_fields=['stock', 'updated_at'])
            return True
        return False

    def add_stock(self, quantity):
        """
        Aumenta el stock del producto.
        
        Args:
            quantity: Cantidad a agregar
        """
        self.stock += quantity
        self.save(update_fields=['stock', 'updated_at'])

    def soft_delete(self):
        """
        Eliminación lógica del producto.
        """
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])


class ProductImage(models.Model):
    """
    Modelo para imágenes adicionales de productos.
    Permite múltiples imágenes por producto.
    """
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='additional_images',
        verbose_name='Producto'
    )
    
    image = models.ImageField(
        upload_to='products/additional/',
        verbose_name='Imagen'
    )
    
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Texto alternativo',
        help_text='Descripción de la imagen para accesibilidad'
    )
    
    is_primary = models.BooleanField(
        default=False,
        verbose_name='Imagen principal',
        help_text='Indica si es la imagen principal del producto'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    class Meta:
        verbose_name = 'Imagen de Producto'
        verbose_name_plural = 'Imágenes de Productos'
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"Imagen de {self.product.name}"

    def save(self, *args, **kwargs):
        """
        Asegura que solo haya una imagen principal por producto.
        """
        if self.is_primary:
            # Desmarcar otras imágenes principales del mismo producto
            ProductImage.objects.filter(
                product=self.product,
                is_primary=True
            ).exclude(id=self.id).update(is_primary=False)
        
        super().save(*args, **kwargs)


