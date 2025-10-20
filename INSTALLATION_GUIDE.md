# 📋 Guía de Instalación - Conexión Backend

Esta guía te ayudará a configurar el backend de Django con PostgreSQL paso a paso.

## 🎯 Objetivo

Crear un backend robusto para el catálogo de productos que se conecte con:
- **Frontend React** (módulo-catalogo)
- **Base de datos PostgreSQL** (PgAdmin 4)
- **Variables de entorno** seguras para GitHub

## 📋 Prerrequisitos

### Software necesario:
- [Python 3.8+](https://www.python.org/downloads/)
- [PostgreSQL 12+](https://www.postgresql.org/download/)
- [PgAdmin 4](https://www.pgadmin.org/download/)
- [Git](https://git-scm.com/downloads)

### Verificar instalaciones:
```bash
python --version
psql --version
git --version
```

## 🚀 Instalación paso a paso

### 1. Preparar el entorno

```bash
# Navegar al directorio del proyecto
cd Conexion-backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
# Instalar paquetes de Python
pip install -r requirements.txt

# Instalar dependencia adicional para el script de verificación
pip install python-dotenv
```

### 3. Configurar PostgreSQL

#### En PgAdmin 4:

1. **Conectar al servidor PostgreSQL**
   - Abrir PgAdmin 4
   - Crear nueva conexión si no existe
   - Host: `localhost`
   - Port: `5432`
   - Username: `postgres`
   - Password: `tu_password` (la que configuraste)

2. **Crear la base de datos**
   ```sql
   -- Ejecutar en PgAdmin 4 Query Tool
   CREATE DATABASE catalogo_db;
   
   -- Verificar que se creó
   \l
   ```

3. **Crear usuario específico (opcional)**
   ```sql
   -- Crear usuario para la aplicación
   CREATE USER catalogo_user WITH PASSWORD 'catalogo_password';
   
   -- Dar permisos completos
   GRANT ALL PRIVILEGES ON DATABASE catalogo_db TO catalogo_user;
   ```

### 4. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar el archivo .env con tus configuraciones
# IMPORTANTE: Nunca subas este archivo a GitHub
```

#### Contenido del archivo .env:
```env
# Base de datos PostgreSQL
DATABASE_NAME=catalogo_db
DATABASE_USER=postgres
DATABASE_PASSWORD=tu_password_aqui
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Django
SECRET_KEY=tu-secret-key-super-segura-de-al-menos-50-caracteres
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS para el frontend React
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Archivos
STATIC_URL=/static/
MEDIA_URL=/media/
MEDIA_ROOT=media/
```

### 5. Configurar el proyecto Django

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones a la base de datos
python manage.py migrate

# Crear superusuario para el panel de administración
python manage.py createsuperuser
```

### 6. Cargar datos de ejemplo (opcional)

```bash
# Ejecutar script de configuración
python setup.py
```

### 7. Verificar la instalación

```bash
# Ejecutar servidor con verificaciones automáticas
python run_server.py

# O ejecutar servidor normal
python manage.py runserver
```

## 🔍 Verificación de la instalación

### 1. Verificar que el servidor funciona
- Visita: http://localhost:8000
- Deberías ver la página de Django

### 2. Verificar el panel de administración
- Visita: http://localhost:8000/admin/
- Inicia sesión con el superusuario creado

### 3. Verificar la API
- Visita: http://localhost:8000/api/docs/
- Deberías ver la documentación de Swagger

### 4. Verificar endpoints específicos
```bash
# Listar categorías
curl http://localhost:8000/api/categories/

# Listar productos
curl http://localhost:8000/api/products/
```

## 🗄️ Estructura de la base de datos

Después de las migraciones, tendrás estas tablas:

```sql
-- Verificar tablas creadas
\dt

-- Deberías ver:
-- auth_group
-- auth_group_permissions
-- auth_permission
-- auth_user
-- auth_user_groups
-- auth_user_user_permissions
-- categories_category
-- django_admin_log
-- django_content_type
-- django_migrations
-- django_session
-- products_product
-- products_productimage
```

## 🔧 Configuración para GitHub

### 1. Archivo .gitignore
Ya está configurado para ignorar:
- `.env` (variables de entorno)
- `__pycache__/` (archivos Python compilados)
- `media/` (archivos subidos)
- `logs/` (archivos de log)

### 2. Variables de entorno en GitHub Actions (opcional)
Si usas GitHub Actions, configura estas variables secretas:
- `DATABASE_NAME`
- `DATABASE_USER`
- `DATABASE_PASSWORD`
- `DATABASE_HOST`
- `SECRET_KEY`

## 🚨 Solución de problemas comunes

### Error: "psycopg2 no se puede importar"
```bash
# Instalar dependencias del sistema (Ubuntu/Debian)
sudo apt-get install python3-dev libpq-dev

# Reinstalar psycopg2
pip uninstall psycopg2-binary
pip install psycopg2-binary
```

### Error: "Base de datos no existe"
```sql
-- En PgAdmin 4, crear la base de datos
CREATE DATABASE catalogo_db;
```

### Error: "Permission denied"
```bash
# Verificar permisos del usuario de PostgreSQL
# En PgAdmin 4, dar permisos completos al usuario
GRANT ALL PRIVILEGES ON DATABASE catalogo_db TO postgres;
```

### Error: "CORS"
```python
# En settings.py, verificar CORS_ALLOWED_ORIGINS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Puerto del frontend React
    'http://127.0.0.1:3000',
]
```

## 📚 Próximos pasos

1. **Conectar con el frontend React**
   - Actualizar la URL de la API en el frontend
   - Probar los endpoints desde el frontend

2. **Personalizar el panel de administración**
   - Agregar más campos a los modelos
   - Personalizar las vistas de administración

3. **Implementar autenticación**
   - JWT tokens para el frontend
   - Permisos por roles de usuario

4. **Agregar tests**
   ```bash
   python manage.py test
   ```

## 🆘 Soporte

Si tienes problemas:

1. **Revisar logs**
   ```bash
   # Ver logs de Django
   tail -f logs/django.log
   ```

2. **Verificar configuración**
   ```bash
   # Verificar configuración de Django
   python manage.py check
   ```

3. **Reiniciar servicios**
   ```bash
   # Reiniciar PostgreSQL (Ubuntu/Debian)
   sudo systemctl restart postgresql
   ```

## ✅ Checklist de instalación

- [ ] Python 3.8+ instalado
- [ ] PostgreSQL instalado y ejecutándose
- [ ] PgAdmin 4 instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] Base de datos `catalogo_db` creada
- [ ] Archivo `.env` configurado
- [ ] Migraciones aplicadas
- [ ] Superusuario creado
- [ ] Servidor ejecutándose en http://localhost:8000
- [ ] Panel de administración accesible
- [ ] API documentación accesible

¡Felicidades! 🎉 Tu backend está listo para conectar con el frontend React.



