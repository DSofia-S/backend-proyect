"""
Vistas para la API de productos.
Proporciona endpoints REST para gestionar productos del catálogo.
"""
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q, F
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, ProductImage
from .serializers import (
    ProductSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductListSerializer,
    ProductStockUpdateSerializer,
    ProductImageSerializer
)


class ProductListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar todos los productos y crear nuevos.
    
    GET: Lista productos con filtros y paginación
    POST: Crea un nuevo producto
    """
    
    queryset = Product.objects.filter(is_active=True).select_related('category')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['name', 'price', 'created_at', 'stock']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Retorna el serializador apropiado según el método HTTP.
        """
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductListSerializer

    def get_queryset(self):
        """
        Filtra los productos según parámetros de búsqueda.
        """
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        # Filtro por rango de precios
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filtro por stock disponible
        in_stock = self.request.query_params.get('in_stock')
        if in_stock and in_stock.lower() == 'true':
            queryset = queryset.filter(stock__gt=0)
        
        # Filtro por categoría
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        
        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para obtener, actualizar o eliminar un producto específico.
    
    GET: Obtiene un producto por ID
    PUT/PATCH: Actualiza un producto
    DELETE: Elimina un producto (soft delete)
    """
    
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    
    def get_serializer_class(self):
        """
        Retorna el serializador apropiado según el método HTTP.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return ProductUpdateSerializer
        return ProductSerializer

    def perform_destroy(self, instance):
        """
        Realiza eliminación lógica en lugar de física.
        """
        instance.soft_delete()


@api_view(['GET'])
def product_search(request):
    """
    Endpoint de búsqueda avanzada de productos.
    
    GET /api/products/search/?q=termo&category=Electrónicos&min_price=100000&max_price=500000
    """
    query = request.query_params.get('q', '')
    category = request.query_params.get('category', '')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')
    in_stock = request.query_params.get('in_stock', 'false').lower() == 'true'
    
    queryset = Product.objects.filter(is_active=True).select_related('category')
    
    # Aplicar filtros
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(sku__icontains=query)
        )
    
    if category:
        queryset = queryset.filter(category__name__icontains=category)
    
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    
    if max_price:
        queryset = queryset.filter(price__lte=max_price)
    
    if in_stock:
        queryset = queryset.filter(stock__gt=0)
    
    # Serializar resultados
    serializer = ProductListSerializer(queryset, many=True)
    
    return Response({
        'results': serializer.data,
        'count': queryset.count(),
        'filters': {
            'query': query,
            'category': category,
            'min_price': min_price,
            'max_price': max_price,
            'in_stock': in_stock
        }
    })


@api_view(['PATCH'])
def update_product_stock(request, product_id):
    """
    Endpoint para actualizar el stock de un producto.
    
    PATCH /api/products/{id}/stock/
    Body: {"stock": 10, "operation": "add|reduce|set"}
    """
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Producto no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = ProductStockUpdateSerializer(data=request.data)
    if serializer.is_valid():
        operation = serializer.validated_data['operation']
        quantity = serializer.validated_data['stock']
        
        if operation == 'add':
            product.add_stock(quantity)
        elif operation == 'reduce':
            if not product.reduce_stock(quantity):
                return Response(
                    {'error': 'Stock insuficiente'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif operation == 'set':
            product.stock = quantity
            product.save(update_fields=['stock', 'updated_at'])
        
        return Response({
            'message': 'Stock actualizado correctamente',
            'product': ProductSerializer(product).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def product_stats(request):
    """
    Endpoint para obtener estadísticas de productos.
    
    GET /api/products/stats/
    """
    total_products = Product.objects.filter(is_active=True).count()
    products_in_stock = Product.objects.filter(is_active=True, stock__gt=0).count()
    out_of_stock = total_products - products_in_stock
    
    # Productos por categoría
    from django.db.models import Count
    products_by_category = Product.objects.filter(is_active=True).values(
        'category__name'
    ).annotate(count=Count('id')).order_by('-count')
    
    # Precio promedio
    from django.db.models import Avg
    avg_price = Product.objects.filter(is_active=True).aggregate(
        avg_price=Avg('price')
    )['avg_price'] or 0
    
    return Response({
        'total_products': total_products,
        'products_in_stock': products_in_stock,
        'out_of_stock': out_of_stock,
        'average_price': round(float(avg_price), 2),
        'products_by_category': list(products_by_category)
    })


class ProductImageView(generics.ListCreateAPIView):
    """
    Vista para gestionar imágenes adicionales de productos.
    """
    
    serializer_class = ProductImageSerializer
    
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductImage.objects.filter(product_id=product_id)
    
    def perform_create(self, serializer):
        product_id = self.kwargs['product_id']
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            serializer.save(product=product)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Producto no encontrado")



