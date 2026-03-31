# 📒 API REST Agenda de Contactos

---

## 📚 Documentación Completa

La documentación está organizada en los siguientes archivos:

1. **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Documentación detallada y completa
2. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Referencia rápida de endpoints
3. **[DETAILED_ENDPOINTS_TABLE.md](DETAILED_ENDPOINTS_TABLE.md)** - Tablas de documentación por endpoint

---

## 🚀 Quick Start

### 1. Instalación

```bash
cd contactos
pip install -r requirements.txt
```

### 2. Inicializar Base de Datos

```bash
sqlite3 agenda.db < agenda_db.sql
```

### 3. Ejecutar Servidor

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Acceder a Documentación Interactiva

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🗄️ Base de Datos

### Motor
- **SQLite3** - Base de datos relacional ligera

### Archivo
- `agenda.db` - Archivo de base de datos

---

## 📋 Tabla: contactos

Estructura de la tabla `contactos`:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_contacto | INTEGER (PK) | Identificador único del contacto |
| nombre | TEXT | Nombre del contacto (máx 100 caracteres) |
| email | TEXT | Correo electrónico del contacto |
| telefono | TEXT | Teléfono del contacto (10 dígitos) |

---

## 🌐 Endpoints API

### 1. GET `/` - Bienvenida
Regresa un mensaje de bienvenida con información de la API.

```bash
curl -X GET "http://localhost:8000/"
```

### 2. GET `/v1/contactos` - Listar Contactos
Retorna una lista paginada de contactos.

```bash
curl -X GET "http://localhost:8000/v1/contactos?limit=10&skip=0"
```

**Parámetros:**
- `limit` (int, default: 10): Límite de registros (1-500)
- `skip` (int, default: 0): Registros a omitir

### 3. GET `/v1/contacto` - Obtener Contacto
Retorna los datos de un contacto por ID o nombre.

```bash
# Por ID
curl -X GET "http://localhost:8000/v1/contacto?id_contacto=1"

# Por nombre
curl -X GET "http://localhost:8000/v1/contacto?nombre=Juan"
```

### 4. POST `/v1/contacto` - Crear Contacto
Inserta un nuevo contacto.

```bash
curl -X POST "http://localhost:8000/v1/contacto" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@gmail.com",
    "telefono": "5510000001"
  }'
```

### 5. PUT `/v1/contacto` - Actualizar Contacto
Modifica un contacto existente.

```bash
curl -X PUT "http://localhost:8000/v1/contacto?id_contacto=1" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez Actualizado",
    "email": "juan.nuevo@gmail.com",
    "telefono": "5510000001"
  }'
```

### 6. DELETE `/v1/contacto` - Eliminar Contacto
Elimina un contacto de la base de datos.

```bash
curl -X DELETE "http://localhost:8000/v1/contacto?id_contacto=1"
```

---

## 📊 Estructura de Respuestas

### Respuesta Exitosa (200/201)

```json
{
  "status": "success",
  "message": "Descripción de la operación",
  "data": { "...": "datos..." },
  "datetime": "30/03/2026 10:30:45"
}
```

### Respuesta de Error (400/404/500)

```json
{
  "status": "error",
  "message": "Descripción del error",
  "data": null,
  "datetime": "30/03/2026 10:30:45"
}
```

---

## 🧪 Testing

### Usar Script de Pruebas Python

```bash
python3 test_api.py
```

El script ejecuta pruebas completas de todos los endpoints.

### Pruebas Manuales con cURL

Ver [QUICK_REFERENCE.md](QUICK_REFERENCE.md) para ejemplos completos de cURL.

---

## 📝 Tabla de Documentación Completa

Para cada endpoint, se documenta:

| No | Propiedad | Descripción |
|----|-----------|-------------|
| 1 | Description | Descripción detallada |
| 2 | Summary | Resumen corto |
| 3 | Version | Versión de la API |
| 4 | Method | Método HTTP |
| 5 | Endpoint | Ruta |
| 6 | Authentication | Tipo de autenticación |
| 7 | Query param | Parámetros de consulta |
| 8 | Path param | Parámetros de ruta |
| 9 | Data | Datos en body |
| 10 | Status code | Código exitoso |
| 11 | Response type | Tipo de respuesta |
| 12 | Response | Estructura de respuesta |
| 13 | Status code (error) | Códigos de error |
| 14 | Response type (error) | Tipo de error |
| 15 | Response (error) | Estructura de error |
| 16 | cURL | Ejemplo cURL |
| 17 | Table | Tabla asociada |

Ver [DETAILED_ENDPOINTS_TABLE.md](DETAILED_ENDPOINTS_TABLE.md) para la documentación completa con tabla de cada endpoint.

---

## 🔑 Características

- ✅ 6 Endpoints CRUD completos
- ✅ Paginación inteligente con limit y skip
- ✅ Búsqueda por ID y nombre
- ✅ Validación automática con Pydantic
- ✅ Manejo robusto de errores
- ✅ Respuestas JSON consistentes
- ✅ Documentación automática Swagger/ReDoc
- ✅ Timezone soporte (America/Mexico_City)
- ✅ SQLite3 para persistencia
- ✅ FastAPI para rendimiento

### Próximas Características (v2.0)
- 🔒 Autenticación JWT
- 🔑 API Key validation
- 📧 Validación de emails avanzada
- 📱 Validación de teléfonos internacionales
- 🔐 Encriptación de datos sensibles
- 📊 Analytics y logging
- 🧪 Pruebas automatizadas
- 🐳 Docker support

---

## 📁 Estructura del Proyecto

```
create_apis/
├── README.md                          # Este archivo
├── API_DOCUMENTATION.md               # Documentación detallada
├── QUICK_REFERENCE.md                 # Referencia rápida
├── DETAILED_ENDPOINTS_TABLE.md        # Tablas de endpoints
├── test_api.py                        # Script de pruebas
└── contactos/
    ├── main.py                        # API FastAPI principal
    ├── app.py                         # Aplicación web
    ├── webapp.py                      # Web framework
    ├── requirements.txt               # Dependencias Python
    ├── agenda_db.sql                  # Script de BD
    ├── agenda.db                      # Base de datos SQLite
    └── templates/
        ├── base.html
        ├── index.html
        ├── create.html
        └── edit.html
```

---

## 🔄 Flujo de Trabajo API

```
┌─────────────────────────────────────────────┐
│           PETICIÓN HTTP                      │
├─────────────────────────────────────────────┤
│  GET /v1/contactos?limit=10&skip=0           │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  FastAPI Router      │
        │  - Validación        │
        │  - Parámetros        │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Función Handler     │
        │  - SQLite connection │
        │  - Query execution   │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Base de Datos       │
        │  (agenda.db)         │
        └──────────┬───────────┘
                   │
                   ▼
     ┌─────────────────────────────┐
     │  RESPUESTA JSON             │
     ├─────────────────────────────┤
     │ {                           │
     │   "status": "success",      │
     │   "message": "...",         │
     │   "data": {...},            │
     │   "datetime": "..."         │
     │ }                           │
     └─────────────────────────────┘
```

---

## 🛠️ Tecnologías Utilizadas

- **FastAPI** - Framework web moderno y rápido
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validación de datos
- **SQLite3** - Base de datos
- **Pytz** - Soporte de zonas horarias
- **Python 3.8+** - Lenguaje de programación

---

## 📄 Licencia

Este proyecto está disponible para uso educativo y comercial.

---

## 👨‍💻 Autor

Desarrollado como parte de un proyecto de API REST con FastAPI.

**Fecha:** 30 de Marzo de 2026

---

## 🤝 Contacto y Soporte

Para más información, consulta los archivos de documentación:
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Documentación completa
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Guía rápida
- [DETAILED_ENDPOINTS_TABLE.md](DETAILED_ENDPOINTS_TABLE.md) - Tablas detalladas

---

## ⚡ Comandos Útiles

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Crear base de datos
```bash
cd contactos
sqlite3 agenda.db < agenda_db.sql
```

### Ejecutar servidor
```bash
cd contactos
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Ejecutar pruebas
```bash
python3 test_api.py
```

### Ver documentación interactiva
```
Abre navgador en: http://localhost:8000/docs
```

---

**¡La API está lista para usar!** 🚀

application/json

| No | Propiedad             | Detalle          |
| -- | --------------------- | ---------------- |
| 11 | Response type         | application/json |
| 12 | Status code (error)   | N/A              |
| 13 | Response type (error) | N/A              |
| 14 | Response (error)      | N/A              |
| 15 | cURL                  | Ver ejemplo      |

curl -X GET http://127.0.0.1:8000/

{
  "message": "Agenda activa",
  "datetime": "29/08/2024"
}
