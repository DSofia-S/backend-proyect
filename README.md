# Conexión Backend - Catálogo de Productos

Backend desarrollado con Django y PostgreSQL para el sistema de catálogo de productos.

## 🚀 Características

- **API REST** completa con Django REST Framework
- **Base de datos PostgreSQL** con PgAdmin 4
- **Gestión de variables de entorno** con django-environ
- **Documentación automática** de la API con drf-spectacular
- **CORS configurado** para el frontend React
- **Panel de administración** personalizado
- **Validaciones** robustas de datos
- **Soft delete** para eliminación lógica
- **Gestión de imágenes** de productos

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 12+
- PgAdmin 4

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd Conexion-backend
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
# Copiar el archivo de ejemplo
cp env.example .env

# Editar el archivo .env con tus configuraciones
```

### 5. Configurar la base de datos

#### En PgAdmin 4:
1. Crear una nueva base de datos llamada `catalogo_db`
2. Crear un usuario con permisos completos (o usar `postgres`)
3. Actualizar las credenciales en el archivo `.env`

#### Ejemplo de configuración en .env:
```env
DATABASE_NAME=catalogo_db
DATABASE_USER=postgres
DATABASE_PASSWORD=tu_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### 6. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear superusuario
```bash
python manage.py createsuperuser
```

### 8. Ejecutar el servidor
```bash
python manage.py runserver
```

## 📚 API Endpoints

### Categorías
- `GET /api/categories/` - Listar categorías
- `POST /api/categories/` - Crear categoría
- `GET /api/categories/{id}/` - Obtener categoría
- `PUT /api/categories/{id}/` - Actualizar categoría
- `DELETE /api/categories/{id}/` - Eliminar categoría
- `GET /api/categories/{id}/products/` - Productos de una categoría
- `GET /api/categories/stats/` - Estadísticas de categorías

### Productos
- `GET /api/products/` - Listar productos
- `POST /api/products/` - Crear producto
- `GET /api/products/{id}/` - Obtener producto
- `PUT /api/products/{id}/` - Actualizar producto
- `DELETE /api/products/{id}/` - Eliminar producto
- `GET /api/products/search/` - Búsqueda avanzada
- `PATCH /api/products/{id}/stock/` - Actualizar stock
- `GET /api/products/stats/` - Estadísticas de productos

### Documentación de la API
- `GET /api/docs/` - Swagger UI
- `GET /api/redoc/` - ReDoc
- `GET /api/schema/` - Esquema OpenAPI

## 🔧 Configuración

### Variables de entorno importantes

```env
# Base de datos
DATABASE_NAME=catalogo_db
DATABASE_USER=postgres
DATABASE_PASSWORD=tu_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Django
SECRET_KEY=tu-secret-key-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS (para el frontend React)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Estructura del proyecto

```
Conexion-backend/
├── catalogo_backend/          # Configuración principal de Django
│   ├── __init__.py
│   ├── settings.py           # Configuración con django-environ
│   ├── urls.py               # URLs principales
│   ├── wsgi.py
│   └── asgi.py
├── products/                  # Aplicación de productos
│   ├── models.py             # Modelos de productos
│   ├── serializers.py        # Serializadores de la API
│   ├── views.py              # Vistas de la API
│   ├── urls.py               # URLs de productos
│   └── admin.py              # Panel de administración
├── categories/                # Aplicación de categorías
│   ├── models.py             # Modelos de categorías
│   ├── serializers.py        # Serializadores de la API
│   ├── views.py              # Vistas de la API
│   ├── urls.py               # URLs de categorías
│   └── admin.py              # Panel de administración
├── requirements.txt           # Dependencias de Python
├── env.example               # Ejemplo de variables de entorno
├── manage.py                 # Script de gestión de Django
└── README.md                 # Este archivo
```

## 🗄️ Modelos de datos

### Product
- `id`: Identificador único
- `name`: Nombre del producto
- `description`: Descripción detallada
- `price`: Precio (DecimalField)
- `category`: Relación con Category
- `image`: Imagen principal
- `stock`: Cantidad en inventario
- `sku`: Código único (generado automáticamente)
- `is_active`: Estado activo/inactivo
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización

### Category
- `id`: Identificador único
- `name`: Nombre de la categoría
- `description`: Descripción opcional
- `is_active`: Estado activo/inactivo
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización

### ProductImage
- `id`: Identificador único
- `product`: Relación con Product
- `image`: Imagen adicional
- `alt_text`: Texto alternativo
- `is_primary`: Imagen principal
- `created_at`: Fecha de creación

## 🔒 Seguridad

- Variables de entorno para datos sensibles
- Validaciones robustas en serializadores
- Soft delete para preservar datos
- CORS configurado específicamente
- Autenticación y permisos de Django

## 🧪 Testing

```bash
# Ejecutar tests
python manage.py test

# Con coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📝 Notas importantes

1. **Base de datos**: Asegúrate de que PostgreSQL esté ejecutándose y que la base de datos `catalogo_db` exista.

2. **Variables de entorno**: Nunca subas el archivo `.env` al repositorio. Usa `env.example` como plantilla.

3. **Migraciones**: Después de cambios en los modelos, ejecuta:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Archivos estáticos**: En producción, recuerda ejecutar:
   ```bash
   python manage.py collectstatic
   ```

5. **CORS**: Si cambias el puerto del frontend, actualiza `CORS_ALLOWED_ORIGINS` en settings.py.

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.



