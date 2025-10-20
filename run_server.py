#!/usr/bin/env python
"""
Script para ejecutar el servidor Django con configuración automática.
Incluye verificación de variables de entorno y configuración de base de datos.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def check_environment():
    """
    Verifica que las variables de entorno estén configuradas correctamente.
    """
    print("Verificando configuracion del entorno...")
    
    # Verificar archivo .env
    if not os.path.exists('.env'):
        print("Archivo .env no encontrado.")
        print("Copia env.example a .env y configura tus variables:")
        print("   cp env.example .env")
        print("   # Luego edita .env con tus configuraciones")
        return False
    
    # Verificar variables críticas
    from decouple import config
    
    required_vars = [
        'SECRET_KEY',
        'DATABASE_NAME',
        'DATABASE_USER',
        'DATABASE_PASSWORD',
        'DATABASE_HOST',
        'DATABASE_PORT'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not config(var, default=None):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("Configura estas variables en tu archivo .env")
        return False
    
    print("Variables de entorno configuradas correctamente")
    return True

def check_database():
    """
    Verifica la conexión a la base de datos.
    """
    print("Verificando conexion a la base de datos...")
    
    try:
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogo_backend.settings')
        django.setup()
        
        # Intentar conectar a la base de datos
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        print("Conexion a la base de datos exitosa")
        return True
        
    except Exception as e:
        print(f"Error de conexion a la base de datos: {e}")
        print("Verifica que:")
        print("   1. PostgreSQL este ejecutandose")
        print("   2. La base de datos 'catalogo' exista")
        print("   3. Las credenciales en .env sean correctas")
        return False

def run_migrations():
    """
    Ejecuta las migraciones si es necesario.
    """
    print("Verificando migraciones...")
    
    try:
        # Verificar si hay migraciones pendientes
        execute_from_command_line(['manage.py', 'showmigrations', '--plan'])
        
        # Aplicar migraciones
        execute_from_command_line(['manage.py', 'migrate'])
        print("Migraciones aplicadas correctamente")
        return True
        
    except Exception as e:
        print(f"Error en migraciones: {e}")
        return False

def main():
    """
    Función principal que ejecuta todas las verificaciones y inicia el servidor.
    """
    print("Iniciando servidor de catalogo de productos...")
    print("=" * 50)
    
    # Verificar entorno
    if not check_environment():
        sys.exit(1)
    
    # Verificar base de datos
    if not check_database():
        sys.exit(1)
    
    # Ejecutar migraciones
    if not run_migrations():
        sys.exit(1)
    
    print("=" * 50)
    print("Todas las verificaciones completadas")
    print("Iniciando servidor en http://localhost:8000")
    print("Documentacion de API: http://localhost:8000/api/docs/")
    print("Panel de administracion: http://localhost:8000/admin/")
    print("=" * 50)
    
    # Iniciar servidor
    try:
        execute_from_command_line(['manage.py', 'runserver'])
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario")
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()



