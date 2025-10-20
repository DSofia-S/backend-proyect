"""
Vistas para la API de categorías.
Proporciona endpoints REST para gestionar categorías.
"""
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Category
from .serializers import (
    CategorySerializer, 
    CategoryCreateSerializer, 
    CategoryUpdateSerializer
)


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar todas las categorías y crear nuevas.
    
    GET: Lista todas las categorías activas
    POST: Crea una nueva categoría
    """
    
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    
    def get_serializer_class(self):
        """
        Retorna el serializador apropiado según el método HTTP.
        """
        if self.request.method == 'POST':
            return CategoryCreateSerializer
        return CategorySerializer

    def get_queryset(self):
        """
        Filtra las categorías según parámetros de búsqueda.
        """
        queryset = Category.objects.filter(is_active=True)
        
        # Filtro por búsqueda en nombre o descripción
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
        
        return queryset.order_by('name')


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para obtener, actualizar o eliminar una categoría específica.
    
    GET: Obtiene una categoría por ID
    PUT/PATCH: Actualiza una categoría
    DELETE: Elimina una categoría (soft delete)
    """
    
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    
    def get_serializer_class(self):
        """
        Retorna el serializador apropiado según el método HTTP.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return CategoryUpdateSerializer
        return CategorySerializer

    def perform_destroy(self, instance):
        """
        Realiza eliminación lógica en lugar de física.
        """
        instance.soft_delete()


@api_view(['GET'])
def category_products(request, category_id):
    """
    Endpoint para obtener todos los productos de una categoría específica.
    
    GET /api/categories/{id}/products/
    """
    try:
        category = Category.objects.get(id=category_id, is_active=True)
    except Category.DoesNotExist:
        return Response(
            {'error': 'Categoría no encontrada'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Obtener productos de la categoría
    products = category.products.filter(is_active=True)
    
    # Serializar productos (necesitarás importar el serializer de productos)
    from products.serializers import ProductSerializer
    serializer = ProductSerializer(products, many=True)
    
    return Response({
        'category': CategorySerializer(category).data,
        'products': serializer.data,
        'count': products.count()
    })


@api_view(['GET'])
def category_stats(request):
    """
    Endpoint para obtener estadísticas de las categorías.
    
    GET /api/categories/stats/
    """
    total_categories = Category.objects.filter(is_active=True).count()
    categories_with_products = Category.objects.filter(
        is_active=True,
        products__is_active=True
    ).distinct().count()
    
    return Response({
        'total_categories': total_categories,
        'categories_with_products': categories_with_products,
        'empty_categories': total_categories - categories_with_products
    })


