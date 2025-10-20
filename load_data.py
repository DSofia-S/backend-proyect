#!/usr/bin/env python
"""
Script para cargar datos de ejemplo en Django.
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogo_backend.settings')
django.setup()

def load_sample_data():
    """
    Carga datos de ejemplo en la base de datos.
    """
    from categories.models import Category
    from products.models import Product
    
    print("Cargando datos de ejemplo...")
    
    # Crear categorías
    categories_data = [
        {'name': 'Electrónicos', 'description': 'Dispositivos electrónicos y tecnología'},
        {'name': 'Ropa', 'description': 'Vestimenta y accesorios'},
        {'name': 'Hogar', 'description': 'Artículos para el hogar'},
        {'name': 'Deportes', 'description': 'Equipos y accesorios deportivos'},
        {'name': 'Libros', 'description': 'Libros y material educativo'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"  Categoria creada: {category.name}")
        else:
            print(f"  Categoria ya existe: {category.name}")
    
    # Crear productos
    products_data = [
        {
            'name': 'iPhone 15 Pro',
            'description': 'El iPhone más avanzado con chip A17 Pro',
            'price': 4500000,
            'category_name': 'Electrónicos',
            'stock': 15
        },
        {
            'name': 'MacBook Air M2',
            'description': 'Laptop ultradelgada con chip M2',
            'price': 6500000,
            'category_name': 'Electrónicos',
            'stock': 8
        },
        {
            'name': 'Camiseta Nike Dri-FIT',
            'description': 'Camiseta deportiva de secado rápido',
            'price': 85000,
            'category_name': 'Ropa',
            'stock': 50
        },
        {
            'name': 'Sofá 3 Puestos Gris',
            'description': 'Sofá moderno de 3 puestos',
            'price': 1200000,
            'category_name': 'Hogar',
            'stock': 3
        },
        {
            'name': 'Pelota de Fútbol Adidas',
            'description': 'Pelota oficial de fútbol',
            'price': 120000,
            'category_name': 'Deportes',
            'stock': 25
        },
        {
            'name': 'Clean Code - Robert Martin',
            'description': 'Libro fundamental sobre programación limpia',
            'price': 85000,
            'category_name': 'Libros',
            'stock': 12
        }
    ]
    
    for prod_data in products_data:
        try:
            category = Category.objects.get(name=prod_data['category_name'])
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'category': category,
                    'stock': prod_data['stock']
                }
            )
            if created:
                print(f"  Producto creado: {product.name}")
            else:
                print(f"  Producto ya existe: {product.name}")
        except Category.DoesNotExist:
            print(f"  Categoria no encontrada: {prod_data['category_name']}")
    
    print("Datos cargados exitosamente!")

if __name__ == '__main__':
    load_sample_data()


