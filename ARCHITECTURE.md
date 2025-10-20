# 🏗️ Arquitectura del Sistema - Catálogo de Productos

## 📊 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   ProductsScreen│  │ ProductCard     │  │ ProductFilters  │ │
│  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│           │                     │                     │         │
│           └─────────────────────┼─────────────────────┘         │
│                                 │                               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                ProductService (API Client)                 │ │
│  │  - GET /api/products/                                      │ │
│  │  - POST /api/products/                                     │ │
│  │  - PUT /api/products/{id}/                                 │ │
│  │  - DELETE /api/products/{id}/                              │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP/HTTPS
                                │ JSON
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (Django REST)                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    URL Routing                             │ │
│  │  - /api/products/     → ProductListCreateView             │ │
│  │  - /api/categories/   → CategoryListCreateView            │ │
│  │  - /api/docs/         → Swagger Documentation             │ │
│  └─────────────────────────────────────────────────────────────┘ │
│           │                     │                     │         │
│           ▼                     ▼                     ▼         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Products App  │  │  Categories App │  │  Admin Panel    │ │
│  │                 │  │                 │  │                 │ │
│  │  - Models       │  │  - Models       │  │  - User Mgmt    │ │
│  │  - Serializers  │  │  - Serializers  │  │  - Data Mgmt    │ │
│  │  - Views        │  │  - Views        │  │  - Monitoring   │ │
│  │  - URLs         │  │  - URLs         │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ ORM (Object-Relational Mapping)
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE (PostgreSQL)                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   products      │  │   categories    │  │   auth_user     │ │
│  │                 │  │                 │  │                 │ │
│  │  - id           │  │  - id           │  │  - id           │ │
│  │  - name         │  │  - name         │  │  - username     │ │
│  │  - description  │  │  - description  │  │  - email        │ │
│  │  - price        │  │  - is_active    │  │  - password     │ │
│  │  - category_id  │  │  - created_at   │  │  - is_superuser │ │
│  │  - image        │  │  - updated_at   │  │  - date_joined  │ │
│  │  - stock        │  │                 │  │                 │ │
│  │  - sku          │  │                 │  │                 │ │
│  │  - is_active    │  │                 │  │                 │ │
│  │  - created_at   │  │                 │  │                 │ │
│  │  - updated_at   │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ product_images  │  │ django_migrations│  │ django_session  │ │
│  │                 │  │                 │  │                 │ │
│  │  - id           │  │  - id           │  │  - session_key  │ │
│  │  - product_id   │  │  - app          │  │  - session_data │ │
│  │  - image        │  │  - name         │  │  - expire_date  │ │
│  │  - alt_text     │  │  - applied      │  │                 │ │
│  │  - is_primary   │  │                 │  │                 │ │
│  │  - created_at   │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Datos

### 1. **Frontend → Backend**
```
React Component → ProductService → HTTP Request → Django View → Serializer → Model → Database
```

### 2. **Backend → Frontend**
```
Database → Model → Serializer → Django View → HTTP Response → ProductService → React Component
```

## 🏛️ Componentes Principales

### **Frontend (React)**
- **ProductsScreen**: Pantalla principal del catálogo
- **ProductCard**: Tarjeta individual de producto
- **ProductFilters**: Filtros de búsqueda
- **ProductService**: Cliente API para comunicación con backend

### **Backend (Django)**
- **URLs**: Enrutamiento de endpoints
- **Views**: Lógica de negocio y manejo de requests
- **Serializers**: Conversión entre JSON y modelos Python
- **Models**: Estructura de datos y relaciones
- **Admin**: Panel de administración

### **Base de Datos (PostgreSQL)**
- **products**: Tabla principal de productos
- **categories**: Tabla de categorías
- **product_images**: Imágenes adicionales de productos
- **auth_user**: Usuarios del sistema
- **django_***: Tablas del sistema Django

## 🔗 Relaciones de Datos

### **Product ↔ Category**
- **Tipo**: Many-to-One (Foreign Key)
- **Relación**: Un producto pertenece a una categoría
- **Implementación**: `category = models.ForeignKey(Category)`

### **Product ↔ ProductImage**
- **Tipo**: One-to-Many (Reverse Foreign Key)
- **Relación**: Un producto puede tener múltiples imágenes
- **Implementación**: `related_name='additional_images'`

## 🛡️ Seguridad

### **Variables de Entorno**
- **SECRET_KEY**: Clave secreta de Django
- **DATABASE_***: Credenciales de base de datos
- **CORS_ALLOWED_ORIGINS**: Orígenes permitidos para CORS

### **Validaciones**
- **Modelos**: Validaciones a nivel de base de datos
- **Serializers**: Validaciones de entrada de datos
- **Views**: Validaciones de lógica de negocio

### **Autenticación**
- **Django Admin**: Autenticación de superusuarios
- **API**: Permisos de lectura/escritura
- **CORS**: Configuración específica de orígenes

## 📊 Endpoints de la API

### **Productos**
```
GET    /api/products/              # Listar productos
POST   /api/products/              # Crear producto
GET    /api/products/{id}/         # Obtener producto
PUT    /api/products/{id}/         # Actualizar producto
DELETE /api/products/{id}/         # Eliminar producto
GET    /api/products/search/       # Búsqueda avanzada
PATCH  /api/products/{id}/stock/   # Actualizar stock
GET    /api/products/stats/        # Estadísticas
```

### **Categorías**
```
GET    /api/categories/            # Listar categorías
POST   /api/categories/            # Crear categoría
GET    /api/categories/{id}/       # Obtener categoría
PUT    /api/categories/{id}/       # Actualizar categoría
DELETE /api/categories/{id}/       # Eliminar categoría
GET    /api/categories/{id}/products/ # Productos de categoría
GET    /api/categories/stats/      # Estadísticas
```

### **Documentación**
```
GET    /api/docs/                  # Swagger UI
GET    /api/redoc/                 # ReDoc
GET    /api/schema/                # Esquema OpenAPI
```

## 🔧 Configuración de Desarrollo

### **Entorno Local**
```bash
# Frontend (puerto 3000)
npm run dev

# Backend (puerto 8000)
python manage.py runserver

# Base de datos (puerto 5432)
PostgreSQL + PgAdmin 4
```

### **Variables de Entorno**
```env
# Base de datos
DATABASE_NAME=catalogo_db
DATABASE_USER=postgres
DATABASE_PASSWORD=tu_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Django
SECRET_KEY=tu-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## 🚀 Despliegue

### **Desarrollo**
- Base de datos local PostgreSQL
- Servidor Django local
- Frontend React local

### **Producción** (futuro)
- Base de datos PostgreSQL en la nube
- Servidor Django en servidor web
- Frontend React en CDN
- Variables de entorno en servidor

## 📈 Escalabilidad

### **Base de Datos**
- Índices en campos de búsqueda
- Paginación en listados
- Soft delete para preservar datos

### **API**
- Caché de respuestas frecuentes
- Rate limiting para prevenir abuso
- Compresión de respuestas

### **Frontend**
- Lazy loading de componentes
- Caché de datos en memoria
- Optimización de imágenes

## 🔍 Monitoreo

### **Logs**
- Logs de Django en `logs/django.log`
- Logs de errores de la aplicación
- Logs de acceso a la API

### **Métricas**
- Estadísticas de productos y categorías
- Tiempo de respuesta de la API
- Uso de la base de datos

Esta arquitectura proporciona una base sólida y escalable para el sistema de catálogo de productos, con separación clara de responsabilidades y facilidad de mantenimiento.



