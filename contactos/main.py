from typing import Optional, Dict, Any
from fastapi import FastAPI, Body, Query, Path, HTTPException
from pydantic import BaseModel, Field, EmailStr
import sqlite3
from datetime import datetime
import pytz
from fastapi.responses import JSONResponse
import traceback

app = FastAPI(title="API Agenda de Contactos", version="1.0.0")

DATABASE = "agenda.db"
ZONA_MX = pytz.timezone("America/Mexico_City")

# ==================== Modelos Pydantic ====================
class Contacto(BaseModel):
    """Modelo de datos para un contacto"""
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del contacto")
    email: EmailStr = Field(..., description="Correo electrónico del contacto")
    telefono: str = Field(..., min_length=10, max_length=10, description="Teléfono del contacto")

class ContactoResponse(Contacto):
    """Modelo de respuesta con ID"""
    id_contacto: int = Field(..., description="ID único del contacto")

# ==================== Utilidades ====================
def get_current_datetime() -> str:
    """Retorna la fecha actual en zona de México"""
    ahora = datetime.now(ZONA_MX)
    return ahora.strftime("%d/%m/%Y %H:%M:%S")

def success_response(data: Any, message: str = "Operación exitosa", status_code: int = 200) -> JSONResponse:
    """Crea una respuesta exitosa"""
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "message": message,
            "data": data,
            "datetime": get_current_datetime()
        }
    )

def error_response(message: str, status_code: int = 400) -> JSONResponse:
    """Crea una respuesta de error"""
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message,
            "data": None,
            "datetime": get_current_datetime()
        }
    )

# ==================== Endpoint 1: GET / ====================
@app.get(
    "/",
    tags=["Root"],
    summary="Bienvenida a la API",
    description="Endpoint raíz que da la bienvenida a la API de contactos",
    responses={
        200: {
            "description": "Bienvenida exitosa",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Bienvenido a la API Agenda de Contactos",
                        "version": "1.0.0",
                        "datetime": "30/03/2026 10:30:45"
                    }
                }
            }
        }
    }
)
async def root():
    """
    ### Descripción
    Endpoint de bienvenida a la API
    
    ### Tabla de Documentación
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
    | 12 | Response | message: string, version: string |
    | 13 | Status code (error) | N/A |
    | 14 | Response type (error) | N/A |
    | 15 | Response (error) | N/A |
    | 16 | cURL | `curl -X GET "http://localhost:8000/"` |
    | 17 | Table | N/A |
    """
    return success_response(
        data={
            "version": "1.0.0",
            "titulo": "API Agenda de Contactos",
            "descripcion": "API REST para gestionar contactos"
        },
        message="Bienvenido a la API Agenda de Contactos"
    )

# ==================== Endpoint 2: GET /v1/contactos ====================
@app.get(
    "/v1/contactos",
    tags=["Contactos"],
    summary="Listar contactos",
    description="Retorna una lista de contactos con paginación",
    responses={
        200: {
            "description": "Lista de contactos obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Contactos obtenidos exitosamente",
                        "data": {
                            "items": [{"id_contacto": 1, "nombre": "Juan", "email": "juan@gmail.com", "telefono": "5510000001"}],
                            "total": 1,
                            "limit": 10,
                            "skip": 0
                        }
                    }
                }
            }
        },
        400: {
            "description": "Parámetros inválidos"
        }
    }
)
async def get_contactos(
    limit: int = Query(10, ge=1, le=500, description="Número máximo de registros a retornar"),
    skip: int = Query(0, ge=0, description="Número de registros a omitir")
):
    """
    ### Descripción
    Obtiene una lista paginada de contactos
    
    ### Tabla de Documentación
    | No | Propiedad | Detalle |
    |---|---|---|
    | 1 | Description | Obtiene lista paginada de contactos |
    | 2 | Summary | Listar contactos |
    | 3 | Version | 1.0.0 |
    | 4 | Method | GET |
    | 5 | Endpoint | `/v1/contactos` |
    | 6 | Authentication | N/A |
    | 7 | Query param | limit, skip |
    | 8 | Path param | N/A |
    | 9 | Data | N/A |
    | 10 | Status code | 200 |
    | 11 | Response type | JSON |
    | 12 | Response | items: array, total: int, limit: int, skip: int |
    | 13 | Status code (error) | 400, 500 |
    | 14 | Response type (error) | JSON |
    | 15 | Response (error) | message: string |
    | 16 | cURL | `curl -X GET "http://localhost:8000/v1/contactos?limit=10&skip=0"` |
    | 17 | Table | contactos |
    """
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Contar total de registros
        cursor.execute("SELECT COUNT(*) as total FROM contactos")
        total = cursor.fetchone()["total"]

        # Obtener contactos con paginación
        cursor.execute(
            "SELECT * FROM contactos LIMIT ? OFFSET ?",
            (limit, skip)
        )
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        conn.close()

        return success_response(
            data={
                "items": items,
                "total": total,
                "limit": limit,
                "skip": skip
            },
            message="Contactos obtenidos exitosamente"
        )

    except Exception as e:
        print(f"Error: {e}\n{traceback.format_exc()}")
        return error_response("Error al obtener los contactos", 500)

# ==================== Endpoint 3: GET /v1/contacto ====================
@app.get(
    "/v1/contacto",
    tags=["Contactos"],
    summary="Obtener contacto",
    description="Retorna los datos de un contacto por id o nombre",
    responses={
        200: {
            "description": "Contacto encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Contacto encontrado",
                        "data": {"id_contacto": 1, "nombre": "Juan", "email": "juan@gmail.com", "telefono": "5510000001"}
                    }
                }
            }
        },
        404: {
            "description": "Contacto no encontrado"
        }
    }
)
async def get_contacto(
    id_contacto: Optional[int] = Query(None, ge=1, description="ID del contacto"),
    nombre: Optional[str] = Query(None, min_length=1, description="Nombre del contacto")
):
    """
    ### Descripción
    Obtiene un contacto específico por ID o nombre
    
    ### Tabla de Documentación
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
    | 12 | Response | id_contacto: int, nombre: string, email: string, telefono: string |
    | 13 | Status code (error) | 400, 404, 500 |
    | 14 | Response type (error) | JSON |
    | 15 | Response (error) | message: string |
    | 16 | cURL | `curl -X GET "http://localhost:8000/v1/contacto?id_contacto=1"` |
    | 17 | Table | contactos |
    """
    try:
        if id_contacto is None and nombre is None:
            return error_response("Se requiere proporcionar id_contacto o nombre", 400)

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if id_contacto is not None:
            cursor.execute("SELECT * FROM contactos WHERE id_contacto = ?", (id_contacto,))
        else:
            cursor.execute("SELECT * FROM contactos WHERE nombre LIKE ?", (f"%{nombre}%",))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return error_response("Contacto no encontrado", 404)

        return success_response(
            data=dict(row),
            message="Contacto encontrado"
        )

    except Exception as e:
        print(f"Error: {e}\n{traceback.format_exc()}")
        return error_response("Error al obtener el contacto", 500)

# ==================== Endpoint 4: POST /v1/contacto ====================
@app.post(
    "/v1/contacto",
    tags=["Contactos"],
    summary="Crear contacto",
    description="Inserta un nuevo contacto",
    status_code=201,
    responses={
        201: {
            "description": "Contacto creado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Contacto creado exitosamente",
                        "data": {"id_contacto": 1, "nombre": "Juan", "email": "juan@gmail.com", "telefono": "5510000001"}
                    }
                }
            }
        },
        400: {
            "description": "Datos inválidos"
        }
    }
)
async def create_contacto(contacto: Contacto = Body(..., description="Datos del contacto a crear")):
    """
    ### Descripción
    Crea un nuevo contacto en la base de datos
    
    ### Tabla de Documentación
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
    | 9 | Data | nombre: string, email: string, telefono: string |
    | 10 | Status code | 201 |
    | 11 | Response type | JSON |
    | 12 | Response | id_contacto: int, nombre: string, email: string, telefono: string |
    | 13 | Status code (error) | 400, 500 |
    | 14 | Response type (error) | JSON |
    | 15 | Response (error) | message: string |
    | 16 | cURL | `curl -X POST "http://localhost:8000/v1/contacto" -H "Content-Type: application/json" -d '{"nombre":"Juan","email":"juan@gmail.com","telefono":"5510000001"}'` |
    | 17 | Table | contactos |
    """
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO contactos (nombre, email, telefono) VALUES (?, ?, ?)",
            (contacto.nombre, contacto.email, contacto.telefono)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        conn.close()

        return success_response(
            data={
                "id_contacto": nuevo_id,
                "nombre": contacto.nombre,
                "email": contacto.email,
                "telefono": contacto.telefono
            },
            message="Contacto creado exitosamente",
            status_code=201
        )

    except Exception as e:
        print(f"Error: {e}\n{traceback.format_exc()}")
        return error_response("Error al crear el contacto", 500)

# ==================== Endpoint 5: PUT /v1/contacto ====================
@app.put(
    "/v1/contacto",
    tags=["Contactos"],
    summary="Actualizar contacto",
    description="Modifica los datos de un contacto existente",
    responses={
        200: {
            "description": "Contacto actualizado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Contacto actualizado exitosamente",
                        "data": {"id_contacto": 1, "nombre": "Juan", "email": "juan@gmail.com", "telefono": "5510000001"}
                    }
                }
            }
        },
        404: {
            "description": "Contacto no encontrado"
        }
    }
)
async def update_contacto(
    id_contacto: int = Query(..., ge=1, description="ID del contacto a actualizar"),
    contacto: Contacto = Body(..., description="Nuevos datos del contacto")
):
    """
    ### Descripción
    Actualiza los datos de un contacto existente
    
    ### Tabla de Documentación
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
    | 9 | Data | nombre: string, email: string, telefono: string |
    | 10 | Status code | 200 |
    | 11 | Response type | JSON |
    | 12 | Response | id_contacto: int, nombre: string, email: string, telefono: string |
    | 13 | Status code (error) | 404, 500 |
    | 14 | Response type (error) | JSON |
    | 15 | Response (error) | message: string |
    | 16 | cURL | `curl -X PUT "http://localhost:8000/v1/contacto?id_contacto=1" -H "Content-Type: application/json" -d '{"nombre":"Juan","email":"juan@gmail.com","telefono":"5510000001"}'` |
    | 17 | Table | contactos |
    """
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Verificar si el contacto existe
        cursor.execute("SELECT * FROM contactos WHERE id_contacto = ?", (id_contacto,))
        if cursor.fetchone() is None:
            conn.close()
            return error_response("Contacto no encontrado", 404)

        # Actualizar contacto
        cursor.execute(
            "UPDATE contactos SET nombre = ?, email = ?, telefono = ? WHERE id_contacto = ?",
            (contacto.nombre, contacto.email, contacto.telefono, id_contacto)
        )
        conn.commit()
        conn.close()

        return success_response(
            data={
                "id_contacto": id_contacto,
                "nombre": contacto.nombre,
                "email": contacto.email,
                "telefono": contacto.telefono
            },
            message="Contacto actualizado exitosamente"
        )

    except Exception as e:
        print(f"Error: {e}\n{traceback.format_exc()}")
        return error_response("Error al actualizar el contacto", 500)

# ==================== Endpoint 6: DELETE /v1/contacto ====================
@app.delete(
    "/v1/contacto",
    tags=["Contactos"],
    summary="Eliminar contacto",
    description="Elimina un contacto de la base de datos",
    responses={
        200: {
            "description": "Contacto eliminado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Contacto eliminado exitosamente",
                        "data": {"id_contacto": 1, "mensaje": "Contacto eliminado"}
                    }
                }
            }
        },
        404: {
            "description": "Contacto no encontrado"
        }
    }
)
async def delete_contacto(
    id_contacto: int = Query(..., ge=1, description="ID del contacto a eliminar")
):
    """
    ### Descripción
    Elimina un contacto de la base de datos
    
    ### Tabla de Documentación
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
    | 12 | Response | id_contacto: int, mensaje: string |
    | 13 | Status code (error) | 404, 500 |
    | 14 | Response type (error) | JSON |
    | 15 | Response (error) | message: string |
    | 16 | cURL | `curl -X DELETE "http://localhost:8000/v1/contacto?id_contacto=1"` |
    | 17 | Table | contactos |
    """
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Verificar si el contacto existe
        cursor.execute("SELECT * FROM contactos WHERE id_contacto = ?", (id_contacto,))
        if cursor.fetchone() is None:
            conn.close()
            return error_response("Contacto no encontrado", 404)

        # Eliminar contacto
        cursor.execute("DELETE FROM contactos WHERE id_contacto = ?", (id_contacto,))
        conn.commit()
        conn.close()

        return success_response(
            data={
                "id_contacto": id_contacto,
                "mensaje": "Contacto eliminado exitosamente"
            },
            message="Contacto eliminado exitosamente"
        )

    except Exception as e:
        print(f"Error: {e}\n{traceback.format_exc()}")
        return error_response("Error al eliminar el contacto", 500)

