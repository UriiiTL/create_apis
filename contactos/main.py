from typing import Annotated

from fastapi import HTTPException
from fastapi import Body, FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import pytz
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get(
    "/", 
    status_code=202,
    summary="Ednpoint raiz",
    description="Bienvenido a la api de agenda"
    )
def get_root():
    response = {
        "message": "Api de la agenda",
        "datatime": "12/02/2026"
        }
    return response

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results




DATABASE = "agenda.db"

@app.get(
    "/v1/contactos",
    summary="Endpoint que regresa los contactos",
    description="""Endpoint que regresa los contactos paginados o permite buscar por id_contacto,
        utiliza los siguientes query paramants:
        limit:int indica el limite de registros a regresar
        skip:int indica el numero de registros a omitir
        id_contacto:int permite buscar un contacto por su ID
    """
)
async def get_contactos(
    limit: int = 10, 
    skip: int = 0, 
):
    try:
        zona_mx = pytz.timezone("America/Mexico_City")
        ahora = datetime.now(zona_mx)
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()

        if limit < 0 or skip < 0:
            conn.close()
            return JSONResponse(
                status_code=400,
                content={
                    "table": "contactos",
                    "items": [],
                    "count": 0,
                    "datetime": ahora.strftime("%d/%m/%Y"),
                    "message": "Los parámetros limit y skip deben ser mayores o iguales a 0",
                    "limit": limit,
                    "skip": skip,
                }
            )
        
        cursor.execute("SELECT COUNT(*) as total FROM contactos")
        total = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT * FROM contactos LIMIT ? OFFSET ?",
            (limit, skip)
        )
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]

        conn.close()

        response = {
            "table": "contactos",
            "items": items,
            "count": len(items),
            "datetime": ahora.strftime("%d/%m/%Y"),
            "message": "Datos consultados exitosamente",
            "limit": limit,
            "skip": skip,
        }

        return JSONResponse(
            status_code=200,
            content=response
        )

    except Exception as e:
        print(f"Error al consultar los contactos: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": "12/02/2026",
                "message": "Error al consultar los contactos",
                "limit": limit,
                "skip": skip,
            }
        )



@app.get(
    "/v1/contacto/{id_contacto}",
    summary="Endpoint que regresa un contacto",
    description="""Endpoint que regresa un contacto por su id_contacto,
        utiliza los siguientes query paramants:
        limit:int indica el limite de registros a regresar
        skip:int indica el numero de registros a omitir
        id_contacto:int permite buscar un contacto por su ID
    """
)
async def get_contacto( 
    id_contacto: int | None = None
):
    try:
        zona_mx = pytz.timezone("America/Mexico_City")
        ahora = datetime.now(zona_mx)
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()

        if (id_contacto is not None and id_contacto < 0):
            conn.close()
            return JSONResponse(
                status_code=400,
                content={
                    "table": "contactos",
                    "items": [],
                    "count": 1,
                    "datetime": ahora.strftime("%d/%m/%Y"),
                    "message": "El parámetro id contacto deben ser mayores a 0",
                    "id_contacto": id_contacto
                }
            )
        if id_contacto is not None:
            cursor.execute(
                "SELECT * FROM contactos WHERE id_contacto = ?",
                (id_contacto,)
            )
            row = cursor.fetchone()

            if row is None:
                conn.close()
                return JSONResponse(
                    status_code=404,
                    content={
                        "table": "contactos",
                        "items": [],
                        "count": 0,
                        "datetime": ahora.strftime("%d/%m/%Y"),
                        "message": "El registro no existe",
                        "id_contacto": id_contacto
                    }
                )

            items = [dict(row)]
            total = 1

        else:
            cursor.execute("SELECT * FROM contactos WHERE id_contacto = ?", (id_contacto,))
            rows = cursor.fetchall()
            items = [dict(row) for row in rows]
            total = len(items)

        conn.close()

        response = {
            "table": "contactos",
            "items": items,
            "count": len(items),
            "datetime": ahora.strftime("%d/%m/%Y"),
            "message": "Datos consultados exitosamente",
            "id_contacto": id_contacto
        }

        return JSONResponse(
            status_code=200,
            content=response
        )

    except Exception as e:
        print(f"Error al consultar los contactos: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": "12/02/2026",
                "message": "Error al consultar los contactos",
                "id_contacto": id_contacto
            }
        )
