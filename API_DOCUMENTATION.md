# 📚 Documentación Completa - API REST Agenda de Contactos

## 📋 Resumen General

**Título:** API Agenda de Contactos  
**Versión:** 1.0.0  
**Framework:** FastAPI  
**Base de Datos:** SQLite3  
**Zona Horaria:** America/Mexico_City

---

## 🗄️ Modelo de Datos

### Tabla: `contactos`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_contacto | INTEGER (PK) | Identificador único del contacto |
| nombre | TEXT | Nombre del contacto (máx 100 caracteres) |
| email | TEXT | Correo electrónico del contacto |
| telefono | TEXT | Teléfono del contacto (10 dígitos) |

### Esquema JSON (Pydantic)

```json
{
  "nombre": "string (1-100 caracteres)",
  "email": "string (formato email)",
  "telefono": "string (10 dígitos)"
}
```

---

## 🌐 Endpoints

### 1️⃣ GET / - Bienvenida a la API

#### Documentación Detallada

| No | Propiedad | Detalle |
|---|---|---|
| 1 | Description | Endpoint de bienvenida a la API |
| 2 | Summary | Bienvenida a la API |
| 3 | Version | 1.0.0 |
| 4 | Method | GET |
| 5 | Endpoint | `/` |
| 6 | Authentication | N/A |
| 7 | Query param | N/A |
| 8 | Path param | N/A |
| 9 | Data | N/A |
| 10 | Status code | 200 |
| 11 | Response type | JSON |
| 12 | Response | { status, message, version, data } |
| 13 | Status code (error) | N/A |
| 14 | Response type (error) | N/A |
| 15 | Response (error) | N/A |
| 16 | cURL | `curl -X GET "http://localhost:8000/"` |
| 17 | Table | N/A |

#### Respuesta Exitosa (200)

```json
{
  "status": "success",
  "message": "Bienvenido a la API Agenda de Contactos",
  "data": {
    "version": "1.0.0",
    "titulo": "API Agenda de Contactos",
    "descripcion": "API REST para gestionar contactos"
  },
  "datetime": "30/03/2026 10:30:45"
}
```

---

### 2️⃣ GET /v1/contactos - Listar Contactos

#### Documentación Detallada

| No | Propiedad | Detalle |
|---|---|---|
| 1 | Description | Obtiene lista paginada de contactos |
| 2 | Summary | Listar contactos |
| 3 | Version | 1.0.0 |
| 4 | Method | GET |
| 5 | Endpoint | `/v1/contactos` |
| 6 | Authentication | N/A |
| 7 | Query param | limit (default: 10), skip (default: 0) |
| 8 | Path param | N/A |
| 9 | Data | N/A |
| 10 | Status code | 200 |
| 11 | Response type | JSON |
| 12 | Response | { status, message, data: { items, total, limit, skip } } |
| 13 | Status code (error) | 400, 500 |
| 14 | Response type (error) | JSON |
| 15 | Response (error) | { status, message, data } |
| 16 | cURL | `curl -X GET "http://localhost:8000/v1/contactos?limit=10&skip=0"` |
| 17 | Table | contactos |

#### Parámetros Query

- **limit** (int, default: 10, 1-500): Número máximo de registros a retornar
- **skip** (int, default: 0, ≥0): Número de registros a omitir

#### Respuesta Exitosa (200)

```json
{
  "status": "success",
  "message": "Contactos obtenidos exitosamente",
  "data": {
    "items": [
      {
        "id_contacto": 1,
        "nombre": "Juan Pérez",
        "email": "juan1@gmail.com",
        "telefono": "5510000001"
      }
    ],
    "total": 50,
    "limit": 10,
    "skip": 0
  },
  "datetime": "30/03/2026 10:30:45"
}
```

#### Respuesta de Error (500)

```json
{
  "status": "error",
  "message": "Error al obtener los contactos",
  "data": null,
  "datetime": "30/03/2026 10:30:45"
}
```

---

### 3️⃣ GET /v1/contacto - Obtener Contacto

#### Documentación Detallada

| No | Propiedad | Detalle |
|---|---|---|
| 1 | Description | Obtiene un contacto por ID o nombre |
| 2 | Summary | Obtener contacto |
| 3 | Version | 1.0.0 |
| 4 | Method | GET |
| 5 | Endpoint | `/v1/contacto` |
| 6 | Authentication | N/A |
| 7 | Query param | id_contacto, nombre |
| 8 | Path param | N/A |
| 9 | Data | N/A |
| 10 | Status code | 200 |
| 11 | Response type | JSON |
| 12 | Response | { status, message, data: {contacto} } |
| 13 | Status code (error) | 400, 404, 500 |
| 14 | Response type (error) | JSON |
| 15 | Response (error) | { status, message, data } |
| 16 | cURL | `curl -X GET "http://localhost:8000/v1/contacto?id_contacto=1"` |
| 17 | Table | contactos |

#### Parámetros Query

- **id_contacto** (int, opcional, ≥1): ID único del contacto
- **nombre** (string, opcional): Nombre del contacto (búsqueda parcial)

**Nota:** Debe proporcionar al menos uno de los parámetros.

#### Respuesta Exitosa (200)

```json
{
  "status": "success",
  "message": "Contacto encontrado",
  "data": {
    "id_contacto": 1,
    "nombre": "Juan Pérez",
    "email": "juan1@gmail.com",
    "telefono": "5510000001"
  },
  "datetime": "30/03/2026 10:30:45"
}
```

#### Respuesta de Error - No Encontrado (404)

```json
{
  "status": "error",
  "message": "Contacto no encontrado",
  "data": null,
  "datetime": "30/03/2026 10:30:45"
}
```

#### Ejemplos de cURL

```bash
# Por ID
curl -X GET "http://localhost:8000/v1/contacto?id_contacto=1"

# Por nombre
curl -X GET "http://localhost:8000/v1/contacto?nombre=Juan"
```

---

### 4️⃣ POST /v1/contacto - Crear Contacto

#### Documentación Detallada

| No | Propiedad | Detalle |
|---|---|---|
| 1 | Description | Crea un nuevo contacto |
| 2 | Summary | Crear contacto |
| 3 | Version | 1.0.0 |
| 4 | Method | POST |
| 5 | Endpoint | `/v1/contacto` |
| 6 | Authentication | N/A |
| 7 | Query param | N/A |
| 8 | Path param | N/A |
| 9 | Data | nombre, email, telefono (JSON body) |
| 10 | Status code | 201 |
| 11 | Response type | JSON |
| 12 | Response | { status, message, data: {contacto creado} } |
| 13 | Status code (error) | 400, 500 |
| 14 | Response type (error) | JSON |
| 15 | Response (error) | { status, message, data } |
| 16 | cURL | `curl -X POST "http://localhost:8000/v1/contacto" -H "Content-Type: application/json" -d '{"nombre":"Juan","email":"juan@gmail.com","telefono":"5510000001"}'` |
| 17 | Table | contactos |

#### Body de Solicitud

```json
{
  "nombre": "Juan Pérez",
  "email": "juan@gmail.com",
  "telefono": "5510000001"
}
```

#### Validaciones

- **nombre**: Requerido, string (1-100 caracteres)
- **email**: Requerido, formato email válido
- **telefono**: Requerido, string de 10 dígitos

#### Respuesta Exitosa (201)

```json
{
  "status": "success",
  "message": "Contacto creado exitosamente",
  "data": {
    "id_contacto": 41,
    "nombre": "Juan Pérez",
    "email": "juan@gmail.com",
    "telefono": "5510000001"
  },
  "datetime": "30/03/2026 10:30:45"
}
```

#### Respuesta de Error (400)

```json
{
  "status": "error",
  "message": "Datos inválidos",
  "data": null,
  "datetime": "30/03/2026 10:30:45"
}
```

#### Ejemplo de cURL

```bash
curl -X POST "http://localhost:8000/v1/contacto" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@gmail.com",
    "telefono": "5510000001"
  }'
```

---

### 5️⃣ PUT /v1/contacto - Actualizar Contacto

#### Documentación Detallada

| No | Propiedad | Detalle |
|---|---|---|
| 1 | Description | Actualiza un contacto existente |
| 2 | Summary | Actualizar contacto |
| 3 | Version | 1.0.0 |
| 4 | Method | PUT |
| 5 | Endpoint | `/v1/contacto` |
| 6 | Authentication | N/A |
| 7 | Query param | id_contacto |
| 8 | Path param | N/A |
| 9 | Data | nombre, email, telefono (JSON body) |
| 10 | Status code | 200 |
| 11 | Response type | JSON |
| 12 | Response | { status, message, data: {contacto actualizado} } |
| 13 | Status code (error) | 404, 500 |
| 14 | Response type (error) | JSON |
| 15 | Response (error) | { status, message, data } |
| 16 | cURL | `curl -X PUT "http://localhost:8000/v1/contacto?id_contacto=1" -H "Content-Type: application/json" -d '{"nombre":"Juan","email":"juan@gmail.com","telefono":"5510000001"}'` |
| 17 | Table | contactos |

#### Parámetros

- **id_contacto** (query, requerido, ≥1): ID del contacto a actualizar

#### Body de Solicitud

```json
{
  "nombre": "Juan Pérez Actualizado",
  "email": "juan.nuevo@gmail.com",
  "telefono": "5510000001"
}
```

#### Respuesta Exitosa (200)

```json
{
  "status": "success",
  "message": "Contacto actualizado exitosamente",
  "data": {
    "id_contacto": 1,
    "nombre": "Juan Pérez Actualizado",
    "email": "juan.nuevo@gmail.com",
    "telefono": "5510000001"
  },
  "datetime": "30/03/2026 10:30:45"
}
```

#### Respuesta de Error - No Encontrado (404)

```json
{
  "status": "error",
  "message": "Contacto no encontrado",
  "data": null,
  "datetime": "30/03/2026 10:30:45"
}
```

#### Ejemplo de cURL

```bash
curl -X PUT "http://localhost:8000/v1/contacto?id_contacto=1" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez Actualizado",
    "email": "juan.nuevo@gmail.com",
    "telefono": "5510000001"
  }'
```

---

### 6️⃣ DELETE /v1/contacto - Eliminar Contacto

#### Documentación Detallada

| No | Propiedad | Detalle |
|---|---|---|
| 1 | Description | Elimina un contacto |
| 2 | Summary | Eliminar contacto |
| 3 | Version | 1.0.0 |
| 4 | Method | DELETE |
| 5 | Endpoint | `/v1/contacto` |
| 6 | Authentication | N/A |
| 7 | Query param | id_contacto |
| 8 | Path param | N/A |
| 9 | Data | N/A |
| 10 | Status code | 200 |
| 11 | Response type | JSON |
| 12 | Response | { status, message, data: {id_contacto, mensaje} } |
| 13 | Status code (error) | 404, 500 |
| 14 | Response type (error) | JSON |
| 15 | Response (error) | { status, message, data } |
| 16 | cURL | `curl -X DELETE "http://localhost:8000/v1/contacto?id_contacto=1"` |
| 17 | Table | contactos |

#### Parámetros

- **id_contacto** (query, requerido, ≥1): ID del contacto a eliminar

#### Respuesta Exitosa (200)

```json
{
  "status": "success",
  "message": "Contacto eliminado exitosamente",
  "data": {
    "id_contacto": 1,
    "mensaje": "Contacto eliminado exitosamente"
  },
  "datetime": "30/03/2026 10:30:45"
}
```

#### Respuesta de Error - No Encontrado (404)

```json
{
  "status": "error",
  "message": "Contacto no encontrado",
  "data": null,
  "datetime": "30/03/2026 10:30:45"
}
```

#### Ejemplo de cURL

```bash
curl -X DELETE "http://localhost:8000/v1/contacto?id_contacto=1"
```

---

## 📊 Códigos de Estado HTTP

| Código | Significado | Descripción |
|--------|-------------|-------------|
| 200 | OK | Solicitud exitosa |
| 201 | Created | Recurso creado exitosamente |
| 400 | Bad Request | Solicitud inválida o parámetros incorrectos |
| 404 | Not Found | Recurso no encontrado |
| 500 | Internal Server Error | Error en el servidor |

---

## 🧪 Ejemplos de Pruebas Completas

### Script de pruebas (tests.sh)

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "=== TEST 1: GET / (Bienvenida) ===" 
curl -X GET "$BASE_URL/"
echo -e "\n\n"

echo "=== TEST 2: GET /v1/contactos (Listar) ==="
curl -X GET "$BASE_URL/v1/contactos?limit=5&skip=0"
echo -e "\n\n"

echo "=== TEST 3: GET /v1/contacto (Obtener por ID) ==="
curl -X GET "$BASE_URL/v1/contacto?id_contacto=1"
echo -e "\n\n"

echo "=== TEST 4: GET /v1/contacto (Obtener por nombre) ==="
curl -X GET "$BASE_URL/v1/contacto?nombre=Juan"
echo -e "\n\n"

echo "=== TEST 5: POST /v1/contacto (Crear) ==="
curl -X POST "$BASE_URL/v1/contacto" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test Usuario",
    "email": "test@gmail.com",
    "telefono": "5510000099"
  }'
echo -e "\n\n"

echo "=== TEST 6: PUT /v1/contacto (Actualizar) ==="
curl -X PUT "$BASE_URL/v1/contacto?id_contacto=1" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez Actualizado",
    "email": "juan.actualizado@gmail.com",
    "telefono": "5510000001"
  }'
echo -e "\n\n"

echo "=== TEST 7: DELETE /v1/contacto (Eliminar) ==="
curl -X DELETE "$BASE_URL/v1/contacto?id_contacto=41"
echo -e "\n\n"
```

---

## 🚀 Cómo Ejecutar

### Requisitos

- Python 3.8+
- FastAPI
- Uvicorn
- SQLite3

### Instalación

```bash
cd /workspaces/create_apis/contactos
pip install -r requirements.txt
```

### Inicializar Base de Datos

```bash
sqlite3 agenda.db < agenda_db.sql
```

### Ejecutar Servidor

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Acceder a Documentación Interactiva

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## 📝 Notas Importantes

1. **Zona Horaria:** Todos los timestamps usan la zona de América/México_City
2. **Validación:** Los datos se validan automáticamente según el esquema Pydantic
3. **Paginación:** Los resultados se limitan a 500 registros máximo por consulta
4. **Seguridad:** No hay autenticación implementada en esta versión (v1.0.0)
5. **CORS:** No está habilitado - considera agregarlo para acceso desde diferentes dominios

---

## ✅ Resumen de Funcionalidades

- ✅ Endpoint raíz de bienvenida
- ✅ Listar contactos con paginación
- ✅ Buscar contacto por ID o nombre
- ✅ Crear nuevo contacto
- ✅ Actualizar contacto existente
- ✅ Eliminar contacto
- ✅ Validación de datos con Pydantic
- ✅ Manejo de errores
- ✅ Respuestas consistentes en JSON
- ✅ Documentación automática en Swagger/ReDoc

