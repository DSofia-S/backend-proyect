#!/usr/bin/env python
"""
Script de configuración simple para el backend Django.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """
    Configuración simple del proyecto Django.
    """
    print("Configuracion del backend Django...")
    print("=" * 50)
    
    # Verificar archivo .env
    if not os.path.exists('.env'):
        print("ERROR: Archivo .env no encontrado!")
        print("Crea el archivo .env con este contenido:")
        print("""
DATABASE_NAME=catalogo_db
DATABASE_USER=postgres
DATABASE_PASSWORD=tu_password_aqui
DATABASE_HOST=localhost
DATABASE_PORT=5432
SECRET_KEY=django-insecure-cambia-esta-clave-por-una-super-segura-de-al-menos-50-caracteres-123456789
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
STATIC_URL=/static/
MEDIA_URL=/media/
MEDIA_ROOT=media/
        """)
        return False
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogo_backend.settings')
    django.setup()
    
    try:
        # Crear superusuario si no existe
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            print("Creando superusuario...")
            print("   Usuario: admin")
            print("   Email: admin@example.com")
            print("   Password: admin123")
            
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
        else:
            print("Superusuario ya existe")
        
        # Cargar datos de ejemplo
        print("Cargando datos de ejemplo...")
        load_sample_data()
        
        print("=" * 50)
        print("Configuracion completada!")
        print("Ejecuta: python manage.py runserver")
        print("Panel admin: http://localhost:8000/admin/")
        print("API docs: http://localhost:8000/api/docs/")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def load_sample_data():
    """
    Carga datos de ejemplo en la base de datos.
    """
    from categories.models import Category
    from products.models import Product
    
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
        except Category.DoesNotExist:
            print(f"  Categoria no encontrada: {prod_data['category_name']}")

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)


