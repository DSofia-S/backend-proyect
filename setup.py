"""
Script de configuración inicial para el proyecto de catálogo.
Ejecuta este script después de la instalación para configurar el proyecto.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_project():
    """
    Configura el proyecto Django inicial.
    """
    print("🚀 Configurando proyecto de catálogo...")
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogo_backend.settings')
    django.setup()
    
    try:
        # Crear migraciones
        print("📝 Creando migraciones...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        # Aplicar migraciones
        print("🗄️ Aplicando migraciones...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Crear superusuario si no existe
        print("👤 Verificando superusuario...")
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            print("⚠️  No se encontró superusuario. Ejecuta:")
            print("   python manage.py createsuperuser")
        else:
            print("✅ Superusuario encontrado")
        
        # Cargar datos de ejemplo
        print("📦 Cargando datos de ejemplo...")
        load_sample_data()
        
        print("✅ ¡Configuración completada!")
        print("\n📋 Próximos pasos:")
        print("1. Ejecuta: python manage.py runserver")
        print("2. Visita: http://localhost:8000/admin/")
        print("3. Visita: http://localhost:8000/api/docs/")
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        sys.exit(1)

def load_sample_data():
    """
    Carga datos de ejemplo en la base de datos.
    """
    from categories.models import Category
    from products.models import Product
    
    # Crear categorías de ejemplo
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
            print(f"  ✅ Categoría creada: {category.name}")
    
    # Crear productos de ejemplo
    products_data = [
        {
            'name': 'iPhone 15 Pro',
            'description': 'El iPhone más avanzado con chip A17 Pro, cámara de 48MP y pantalla Super Retina XDR de 6.1 pulgadas.',
            'price': 4500000,
            'category_name': 'Electrónicos',
            'stock': 15
        },
        {
            'name': 'MacBook Air M2',
            'description': 'Laptop ultradelgada con chip M2, pantalla Liquid Retina de 13.6 pulgadas y hasta 18 horas de batería.',
            'price': 6500000,
            'category_name': 'Electrónicos',
            'stock': 8
        },
        {
            'name': 'Camiseta Nike Dri-FIT',
            'description': 'Camiseta deportiva de secado rápido con tecnología Dri-FIT para máximo rendimiento.',
            'price': 85000,
            'category_name': 'Ropa',
            'stock': 50
        },
        {
            'name': 'Sofá 3 Puestos Gris',
            'description': 'Sofá moderno de 3 puestos en tela gris, perfecto para salas contemporáneas.',
            'price': 1200000,
            'category_name': 'Hogar',
            'stock': 3
        },
        {
            'name': 'Pelota de Fútbol Adidas',
            'description': 'Pelota oficial de fútbol Adidas, ideal para partidos y entrenamientos.',
            'price': 120000,
            'category_name': 'Deportes',
            'stock': 25
        },
        {
            'name': 'Clean Code - Robert Martin',
            'description': 'Libro fundamental sobre programación limpia y buenas prácticas de desarrollo.',
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
                print(f"  ✅ Producto creado: {product.name}")
        except Category.DoesNotExist:
            print(f"  ⚠️  Categoría no encontrada: {prod_data['category_name']}")

if __name__ == '__main__':
    setup_project()



