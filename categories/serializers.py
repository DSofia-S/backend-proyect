"""
Serializadores para la API de categorías.
Convierte los modelos Django a JSON y viceversa.
"""
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Category.
    """
    
    # Campo calculado para mostrar el número de productos
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'is_active',
            'created_at',
            'updated_at',
            'products_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_products_count(self, obj):
        """
        Calcula el número de productos en la categoría.
        """
        return obj.get_products_count()

    def validate_name(self, value):
        """
        Valida que el nombre de la categoría sea único.
        """
        if self.instance and self.instance.name == value:
            return value
            
        if Category.objects.filter(name=value, is_active=True).exists():
            raise serializers.ValidationError(
                "Ya existe una categoría activa con este nombre."
            )
        return value


class CategoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializador específico para crear categorías.
    """
    
    class Meta:
        model = Category
        fields = ['name', 'description']

    def validate_name(self, value):
        """
        Valida que el nombre sea único al crear.
        """
        if Category.objects.filter(name=value, is_active=True).exists():
            raise serializers.ValidationError(
                "Ya existe una categoría activa con este nombre."
            )
        return value


class CategoryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador específico para actualizar categorías.
    """
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']

    def validate_name(self, value):
        """
        Valida que el nombre sea único al actualizar.
        """
        if self.instance and self.instance.name == value:
            return value
            
        if Category.objects.filter(name=value, is_active=True).exists():
            raise serializers.ValidationError(
                "Ya existe una categoría activa con este nombre."
            )
        return value


