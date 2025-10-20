"""
Configuración de URLs para la aplicación de productos.
"""
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Lista y creación de productos
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    
    # Detalle, actualización y eliminación de productos
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Búsqueda avanzada de productos
    path('products/search/', views.product_search, name='product-search'),
    
    # Actualización de stock
    path('products/<int:product_id>/stock/', views.update_product_stock, name='product-stock-update'),
    
    # Estadísticas de productos
    path('products/stats/', views.product_stats, name='product-stats'),
    
    # Gestión de imágenes de productos
    path('products/<int:product_id>/images/', views.ProductImageView.as_view(), name='product-images'),
]



