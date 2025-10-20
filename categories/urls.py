"""
Configuración de URLs para la aplicación de categorías.
"""
from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    # Lista y creación de categorías
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    
    # Detalle, actualización y eliminación de categorías
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Productos de una categoría específica
    path('categories/<int:category_id>/products/', views.category_products, name='category-products'),
    
    # Estadísticas de categorías
    path('categories/stats/', views.category_stats, name='category-stats'),
]


