"""
Serializadores para la API de productos.
Convierte los modelos Django a JSON y viceversa.
"""
from rest_framework import serializers
from .models import Product, ProductImage
from categories.serializers import CategorySerializer


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializador para imágenes adicionales de productos.
    """
    
    class Meta:
        model = ProductImage
        fields = [
            'id',
            'image',
            'alt_text',
            'is_primary',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializador principal para el modelo Product.
    """
    
    # Campos calculados
    price_display = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()
    
    # Relaciones
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    # Imágenes adicionales
    additional_images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'price_display',
            'category',
            'category_id',
            'image',
            'additional_images',
            'stock',
            'sku',
            'is_active',
            'is_in_stock',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'sku', 'created_at', 'updated_at']

    def get_price_display(self, obj):
        """
        Retorna el precio formateado como moneda.
        """
        return obj.get_price_display()

    def get_is_in_stock(self, obj):
        """
        Verifica si el producto tiene stock disponible.
        """
        return obj.is_in_stock()

    def validate_category_id(self, value):
        """
        Valida que la categoría exista y esté activa.
        """
        from categories.models import Category
        try:
            category = Category.objects.get(id=value, is_active=True)
        except Category.DoesNotExist:
            raise serializers.ValidationError(
                "La categoría especificada no existe o no está activa."
            )
        return value

    def validate_stock(self, value):
        """
        Valida que el stock no sea negativo.
        """
        if value < 0:
            raise serializers.ValidationError(
                "El stock no puede ser negativo."
            )
        return value

    def validate_price(self, value):
        """
        Valida que el precio sea positivo.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "El precio debe ser mayor a cero."
            )
        return value


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Serializador específico para crear productos.
    """
    
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'category_id',
            'image',
            'stock'
        ]

    def validate_category_id(self, value):
        """
        Valida que la categoría exista y esté activa.
        """
        from categories.models import Category
        try:
            category = Category.objects.get(id=value, is_active=True)
        except Category.DoesNotExist:
            raise serializers.ValidationError(
                "La categoría especificada no existe o no está activa."
            )
        return value


class ProductUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador específico para actualizar productos.
    """
    
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'category_id',
            'image',
            'stock',
            'is_active'
        ]

    def validate_category_id(self, value):
        """
        Valida que la categoría exista y esté activa.
        """
        from categories.models import Category
        try:
            category = Category.objects.get(id=value, is_active=True)
        except Category.DoesNotExist:
            raise serializers.ValidationError(
                "La categoría especificada no existe o no está activa."
            )
        return value


class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado para listar productos.
    """
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    price_display = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'price_display',
            'category_name',
            'image',
            'stock',
            'is_in_stock',
            'created_at'
        ]

    def get_price_display(self, obj):
        return obj.get_price_display()

    def get_is_in_stock(self, obj):
        return obj.is_in_stock()


class ProductStockUpdateSerializer(serializers.Serializer):
    """
    Serializador para actualizar solo el stock de un producto.
    """
    
    stock = serializers.IntegerField(min_value=0)
    operation = serializers.ChoiceField(choices=['add', 'reduce', 'set'])

    def validate(self, data):
        """
        Valida la operación de stock.
        """
        operation = data.get('operation')
        stock = data.get('stock')
        
        if operation == 'reduce' and stock <= 0:
            raise serializers.ValidationError(
                "La cantidad a reducir debe ser mayor a cero."
            )
        
        return data



