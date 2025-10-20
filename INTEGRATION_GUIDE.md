# 🔗 Guía de Integración Frontend-Backend

Esta guía te ayudará a conectar tu frontend React con el backend Django paso a paso.

## 📋 Pasos para la Integración

### 1. **Configurar el Backend Django**

#### a) Crear archivo .env
Crea el archivo `.env` en la carpeta `Conexion-backend` con este contenido:

```env
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
```

#### b) Configurar PostgreSQL
1. Abrir PgAdmin 4
2. Crear base de datos `catalogo_db`
3. Actualizar la contraseña en el archivo `.env`

#### c) Ejecutar configuración rápida
```bash
cd Conexion-backend
python quick_setup.py
```

#### d) Iniciar servidor Django
```bash
python manage.py runserver
```

### 2. **Configurar el Frontend React**

#### a) Instalar dependencias (si no están instaladas)
```bash
cd modulo-catalogo
npm install
```

#### b) Iniciar servidor React
```bash
npm run dev
```

### 3. **Verificar la Integración**

1. **Abrir el navegador** en `http://localhost:3000`
2. **Ver el componente de prueba** que muestra el estado de conexión
3. **Revisar la consola** del navegador para ver los logs
4. **Probar los endpoints** manualmente:
   - `http://localhost:8000/api/categories/`
   - `http://localhost:8000/api/products/`
   - `http://localhost:8000/api/docs/`

## 🔧 Solución de Problemas Comunes

### Error: "CORS policy"
**Solución:**
```python
# En Conexion-backend/catalogo_backend/settings.py
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
```

### Error: "Connection refused"
**Solución:**
1. Verificar que Django esté ejecutándose en puerto 8000
2. Verificar que React esté ejecutándose en puerto 3000
3. Revisar la URL en `modulo-catalogo/src/services/api.ts`

### Error: "Database connection"
**Solución:**
1. Verificar que PostgreSQL esté ejecutándose
2. Verificar las credenciales en `.env`
3. Ejecutar migraciones: `python manage.py migrate`

### Error: "No data returned"
**Solución:**
1. Ejecutar `python quick_setup.py` para cargar datos de ejemplo
2. Verificar que las tablas existan en la base de datos
3. Revisar los logs de Django

## 📊 Endpoints Disponibles

### Categorías
- `GET /api/categories/` - Listar categorías
- `POST /api/categories/` - Crear categoría
- `GET /api/categories/{id}/` - Obtener categoría
- `PUT /api/categories/{id}/` - Actualizar categoría
- `DELETE /api/categories/{id}/` - Eliminar categoría

### Productos
- `GET /api/products/` - Listar productos
- `POST /api/products/` - Crear producto
- `GET /api/products/{id}/` - Obtener producto
- `PUT /api/products/{id}/` - Actualizar producto
- `DELETE /api/products/{id}/` - Eliminar producto
- `GET /api/products/search/` - Búsqueda avanzada

### Documentación
- `GET /api/docs/` - Swagger UI
- `GET /api/redoc/` - ReDoc

## 🧪 Pruebas de Integración

### 1. Prueba de Conexión
El componente `BackendTest` en React verifica:
- ✅ Conexión con Django
- ✅ Carga de categorías
- ✅ Carga de productos
- ✅ Manejo de errores

### 2. Pruebas Manuales
```bash
# Probar categorías
curl http://localhost:8000/api/categories/

# Probar productos
curl http://localhost:8000/api/products/

# Probar búsqueda
curl "http://localhost:8000/api/products/search/?q=iPhone"
```

### 3. Pruebas en el Navegador
1. Abrir `http://localhost:3000`
2. Ver el estado de conexión
3. Probar filtros de productos
4. Verificar que los datos se cargan correctamente

## 📝 Logs y Debugging

### Backend (Django)
```bash
# Ver logs de Django
tail -f Conexion-backend/logs/django.log

# Modo debug
python manage.py runserver --verbosity=2
```

### Frontend (React)
1. Abrir DevTools (F12)
2. Ir a la pestaña Console
3. Ver logs de conexión y errores
4. Revisar la pestaña Network para ver las peticiones

## 🚀 Próximos Pasos

Una vez que la integración funcione:

1. **Remover el componente de prueba** `BackendTest`
2. **Implementar autenticación** si es necesario
3. **Agregar validaciones** en el frontend
4. **Implementar manejo de errores** más robusto
5. **Agregar tests** automatizados

## 📞 Soporte

Si tienes problemas:

1. **Revisar logs** de Django y React
2. **Verificar configuración** de CORS
3. **Probar endpoints** manualmente
4. **Revisar la consola** del navegador

¡La integración debería funcionar perfectamente siguiendo estos pasos! 🎉
