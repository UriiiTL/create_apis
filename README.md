# 📒 API Agenda

Proyecto de una API básica para una agenda de contactos.
Incluye definición de base de datos, endpoint raíz y documentación del endpoint.

---

## 🗄️ Base de Datos

### Motor
- SQLite3

### Archivo
- `agenda.db`

---

## 📋 Tabla: contactos

Estructura de la tabla `contactos`:

| Campo        | Tipo          | Descripción |
|-------------|---------------|-------------|
| id_contacto | INT (PK)      | Identificador del contacto |
| nombre      | VARCHAR(100)  | Nombre del contacto |
| email       | VARCHAR(100)  | Correo electrónico |
| telefono    | VARCHAR(10)   | Teléfono del contacto |

---

## 🌐 Documentación

La documentación del proyecto se encuentra disponible en:

```text
http://localhost:8000/docs


| No | Propiedad      | Detalle                            |
| -- | -------------- | ---------------------------------- |
| 1  | Description    | Endpoint de bienvenida             |
| 2  | Summary        | Endpoint de bienvenida a la agenda |
| 3  | Method         | GET                                |
| 4  | Endpoint       | `/`                                |
| 5  | Authentication | N/A                                |
| 6  | Query param    | N/A                                |
| 7  | Path param     | N/A                                |
| 8  | Data           | N/A                                |
| 9  | Status code    | 202                                |
| 10 | Response       | JSON                               |

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
