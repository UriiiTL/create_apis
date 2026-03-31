# 📖 Documentación Detallada por Endpoints - Tabla Completa

## 📌 ESTRUCTURA DE LA TABLA DE DOCUMENTACIÓN

| No | Propiedad | Descripción |
|----|-----------|------------|
| 1 | Description | Descripción detallada del endpoint |
| 2 | Summary | Resumen corto del endpoint |
| 3 | Version | Versión de la API |
| 4 | Method | Método HTTP (GET, POST, PUT, DELETE) |
| 5 | Endpoint | Ruta del endpoint |
| 6 | Authentication | Tipo de autenticación requerida |
| 7 | Query param | Parámetros de consulta |
| 8 | Path param | Parámetros de ruta |
| 9 | Data | Datos en el body de la solicitud |
| 10 | Status code | Código de estado exitoso |
| 11 | Response type | Tipo de respuesta (JSON, XML, etc) |
| 12 | Response | Estructura de la respuesta exitosa |
| 13 | Status code (error) | Códigos de estado de error |
| 14 | Response type (error) | Tipo de respuesta de error |
| 15 | Response (error) | Estructura de respuesta de error |
| 16 | cURL | Ejemplo con cURL |
| 17 | Table | Tabla de base de datos asociada |

---

## 🔴 ENDPOINT 1: GET / - BIENVENIDA A LA API

| No | Propiedad | Detalle |
|---|---|---|
| 1 | Description | Endpoint de bienvenida que proporciona información sobre la API |
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
| 12 | Response | `{ "status": "success", "message": "Bienvenido a la API Agenda de Contactos", "data": { "version": "1.0.0", "titulo": "API Agenda de Contactos", "descripcion": "API REST para gestionar contactos" }, "datetime": "30/03/2026 10:30:45" }` |
| 13 | Status code (error) | N/A |
| 14 | Response type (error) | N/A |
| 15 | Response (error) | N/A |
| 16 | cURL | `curl -X GET "http://localhost:8000/"` |
| 17 | Table | N/A |

**Ejemplo de Respuesta:**
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

## 🔵 ENDPOINT 2: GET /v1/contactos - LISTAR CONTACTOS

| No | Propiedad | Detalle |
|---|---|---|
| 1 | Description | Obtiene una lista paginada de contactos de la base de datos |
| 2 | Summary | Listar contactos |
| 3 | Version | 1.0.0 |
| 4 | Method | GET |
| 5 | Endpoint | `/v1/contactos` |
| 6 | Authentication | N/A |
| 7 | Query param | `limit` (int, default: 10, rango: 1-500), `skip` (int, default: 0, mín: 0) |
| 8 | Path param | N/A |
| 9 | Data | N/A |
| 10 | Status code | 200 |
| 11 | Response type | JSON |
| 12 | Response | `{ "status": "success", "message": "Contactos obtenidos exitosamente", "data": { "items": [{ "id_contacto": int, "nombre": string, "email": string, "telefono": string }], "total": int, "limit": int, "skip": int }, "datetime": string }` |
| 13 | Status code (error) | 400, 500 |
| 14 | Response type (error) | JSON |
| 15 | Response (error) | `{ "status": "error", "message": string, "data": null, "datetime": string }` |
| 16 | cURL | `curl -X GET "http://localhost:8000/v1/contactos?limit=10&skip=0"` |
| 17 | Table | contactos |

**Parámetros de Query:**
- `limit`: Número máximo de registros a retornar (1-500, default: 10)
- `skip`: Número de registros a omitir para paginación (≥0, default: 0)

**Ejemplo de Respuesta Exitosa (200):**
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
      },
      {
        "id_contacto": 2,
        "nombre": "María López",
        "email": "maria2@gmail.com",
        "telefono": "5510000002"
      }
    ],
    "total": 50,
    "limit": 10,
    "skip": 0
  },
  "datetime": "30/03/2026 10:30:45"
}
```

**Ejemplo de Respuesta de Error (500):**
```json
{
  "status": "error",
  "message": "Error al obtener los contactos",
  "data": null,
  "datetime": "30/03/2026 10:30:45"
}
```

---

## 🟢 ENDPOINT 3: GET /v1/contacto - OBTENER CONTACTO ESPECÍFICO

| No | Propiedad | Detalle |
|---|---|---|
| 1 | Description | Obtiene los datos de un contacto específico por ID o nombre |
| 2 | Summary | Obtener contacto |
| 3 | Version | 1.0.0 |
| 4 | Method | GET |
| 5 | Endpoint | `/v1/contacto` |
| 6 | Authentication | N/A |
| 7 | Query param | `id_contacto` (int, opcional, ≥1), `nombre` (string, opcional) - Uno requerido |
| 8 | Path param | N/A |
| 9 | Data | N/A |
| 10 | Status code | 200 |
| 11 | Response type | JSON |
| 12 | Response | `{ "status": "success", "message": "Contacto encontrado", "data": { "id_contacto": int, "nombre": string, "email": string, "telefono": string }, "datetime": string }` |
| 13 | Status code (error) | 400, 404, 500 |
| 14 | Response type (error) | JSON |
| 15 | Response (error) | `{ "status": "error", "message": string, "data": null, "datetime": string }` |
| 16 | cURL | `curl -X GET "http://localhost:8000/v1/contacto?id_contacto=1"` o `curl -X GET "http://localhost:8000/v1/contacto?nombre=Juan"` |
| 17 | Table | contactos |

**Parámetros de Query (Uno Requerido):**
- `id_contacto`: ID del contacto (entero ≥1)
- `nombre`: Nombre del contacto (búsqueda parcial)

**Ejemplo de Respuesta Exitosa (200):**
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

**Ejemplo de Respuesta de Error - No Encontrado (404):**
```json
{
  "status": "error",
  "message": "Contacto no encontrado",
  "data": null,
  "datetime": "30/03/2026 10:30:45"
}
```

**Ejemplos de cURL:**
```bash
# Por ID
curl -X GET "http://localhost:8000/v1/contacto?id_contacto=1"

# Por nombre
curl -X GET "http://localhost:8000/v1/contacto?nombre=Juan"
```

---

## 🟡 ENDPOINT 4: POST /v1/contacto - CREAR CONTACTO

| No | Propiedad | Detalle |
|---|---|---|
| 1 | Description | Inserta un nuevo contacto en la base de datos |
| 2 | Summary | Crear contacto |
| 3 | Version | 1.0.0 |
| 4 | Method | POST |
| 5 | Endpoint | `/v1/contacto` |
| 6 | Authentication | N/A |
| 7 | Query param | N/A |
| 8 | Path param | N/A |
| 9 | Data | `{ "nombre": string (1-100), "email": string (email válido), "telefono": string (10 dígitos) }` |
| 10 | Status code | 201 |
| 11 | Response type | JSON |
| 12 | Response | `{ "status": "success", "message": "Contacto creado exitosamente", "data": { "id_contacto": int, "nombre": string, "email": string, "telefono": string }, "datetime": string }` |
| 13 | Status code (error) | 400, 500 |
| 14 | Response type (error) | JSON |
| 15 | Response (error) | `{ "status": "error", "message": string, "data": null, "datetime": string }` |
| 16 | cURL | `curl -X POST "http://localhost:8000/v1/contacto" -H "Content-Type: application/json" -d '{"nombre":"Juan Pérez","email":"juan@gmail.com","telefono":"5510000001"}'` |
| 17 | Table | contactos |

**Body de Solicitud (JSON):**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@gmail.com",
  "telefono": "5510000001"
}
```

**Validaciones:**
- `nombre`: Requerido, texto de 1-100 caracteres
- `email`: Requerido, formato de email válido
- `telefono`: Requerido, exactamente 10 dígitos

**Ejemplo de Respuesta Exitosa (201):**
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

**Ejemplo de Respuesta de Error (400):**
```json
{
  "status": "error",
  "message": "Datos inválidos",
  "data": null,
  "datetime": "30/03/2026 10:30:45"
}
```

**Ejemplo de cURL:**
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

## 🟣 ENDPOINT 5: PUT /v1/contacto - ACTUALIZAR CONTACTO

| No | Propiedad | Detalle |
|---|---|---|
| 1 | Description | Modifica los datos de un contacto existente |
| 2 | Summary | Actualizar contacto |
| 3 | Version | 1.0.0 |
| 4 | Method | PUT |
| 5 | Endpoint | `/v1/contacto` |
| 6 | Authentication | N/A |
| 7 | Query param | `id_contacto` (int, requerido, ≥1) |
| 8 | Path param | N/A |
| 9 | Data | `{ "nombre": string (1-100), "email": string (email válido), "telefono": string (10 dígitos) }` |
| 10 | Status code | 200 |
| 11 | Response type | JSON |
| 12 | Response | `{ "status": "success", "message": "Contacto actualizado exitosamente", "data": { "id_contacto": int, "nombre": string, "email": string, "telefono": string }, "datetime": string }` |
| 13 | Status code (error) | 404, 500 |
| 14 | Response type (error) | JSON |
| 15 | Response (error) | `{ "status": "error", "message": string, "data": null, "datetime": string }` |
| 16 | cURL | `curl -X PUT "http://localhost:8000/v1/contacto?id_contacto=1" -H "Content-Type: application/json" -d '{"nombre":"Juan Pérez Actualizado","email":"juan.nuevo@gmail.com","telefono":"5510000001"}'` |
| 17 | Table | contactos |

**Parámetros de Query:**
- `id_contacto`: ID del contacto a actualizar (entero ≥1, requerido)

**Body de Solicitud (JSON):**
```json
{
  "nombre": "Juan Pérez Actualizado",
  "email": "juan.nuevo@gmail.com",
  "telefono": "5510000001"
}
```

**Ejemplo de Respuesta Exitosa (200):**
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

**Ejemplo de Respuesta de Error - No Encontrado (404):**
```json
{
  "status": "error",
  "message": "Contacto no encontrado",
  "data": null,
  "datetime": "30/03/2026 10:30:45"
}
```

**Ejemplo de cURL:**
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

## 🔴 ENDPOINT 6: DELETE /v1/contacto - ELIMINAR CONTACTO

| No | Propiedad | Detalle |
|---|---|---|
| 1 | Description | Elimina un contacto de la base de datos |
| 2 | Summary | Eliminar contacto |
| 3 | Version | 1.0.0 |
| 4 | Method | DELETE |
| 5 | Endpoint | `/v1/contacto` |
| 6 | Authentication | N/A |
| 7 | Query param | `id_contacto` (int, requerido, ≥1) |
| 8 | Path param | N/A |
| 9 | Data | N/A |
| 10 | Status code | 200 |
| 11 | Response type | JSON |
| 12 | Response | `{ "status": "success", "message": "Contacto eliminado exitosamente", "data": { "id_contacto": int, "mensaje": string }, "datetime": string }` |
| 13 | Status code (error) | 404, 500 |
| 14 | Response type (error) | JSON |
| 15 | Response (error) | `{ "status": "error", "message": string, "data": null, "datetime": string }` |
| 16 | cURL | `curl -X DELETE "http://localhost:8000/v1/contacto?id_contacto=1"` |
| 17 | Table | contactos |

**Parámetros de Query:**
- `id_contacto`: ID del contacto a eliminar (entero ≥1, requerido)

**Ejemplo de Respuesta Exitosa (200):**
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

**Ejemplo de Respuesta de Error - No Encontrado (404):**
```json
{
  "status": "error",
  "message": "Contacto no encontrado",
  "data": null,
  "datetime": "30/03/2026 10:30:45"
}
```

**Ejemplo de cURL:**
```bash
curl -X DELETE "http://localhost:8000/v1/contacto?id_contacto=1"
```

---

## 📊 RESUMEN COMPARATIVO DE ENDPOINTS

| Endpoint | Método | Propósito | Parámetros | Body | Status OK | Status Error |
|----------|--------|----------|-----------|------|-----------|--------------|
| `/` | GET | Bienvenida | - | - | 200 | N/A |
| `/v1/contactos` | GET | Listar paginado | limit, skip | - | 200 | 400, 500 |
| `/v1/contacto` | GET | Obtener uno | id_contacto, nombre | - | 200 | 400, 404, 500 |
| `/v1/contacto` | POST | Crear | - | nombre, email, telefono | 201 | 400, 500 |
| `/v1/contacto` | PUT | Actualizar | id_contacto | nombre, email, telefono | 200 | 404, 500 |
| `/v1/contacto` | DELETE | Eliminar | id_contacto | - | 200 | 404, 500 |

---

## 🔑 CONVENCIONES

1. **Tipo de Autenticación:** Ninguna en v1.0.0
2. **Formato de Respuesta:** JSON con estructura consistente
3. **Zona Horaria:** America/Mexico_City
4. **Validación:** Automática con Pydantic
5. **Base de Datos:** SQLite3 (agenda.db)

