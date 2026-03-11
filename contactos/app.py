from fastapi.testclient import TestClient
from main import app  # Asegúrate de que apunte a donde está definida tu instancia FastAPI

client = TestClient(app)

# TODO: 1. GET 202 /v1/contactos?limit=10&skip=0 primeros 10 contactos 
def test_get_contactos_limit_10_skip_0():
    response = client.get("/v1/contactos?limit=10&skip=0")
    data ={
            "table":"contactos",
            "items":[
                        {"id_contacto": 1, "nombre": "Juan Pérez", "telefono": "5510000001", "email": "juan1@gmail.com"},    
                        {"id_contacto": 2, "nombre": "María López", "telefono": "5510000002", "email": "maria2@gmail.com"},
                        {"id_contacto": 3, "nombre": "Carlos Sánchez", "telefono": "5510000003", "email": "carlos3@gmail.com"},
                        {"id_contacto": 4, "nombre": "Ana Torres", "telefono": "5510000004", "email": "ana4@gmail.com"},
                        {"id_contacto": 5, "nombre": "Luis Ramírez", "telefono": "5510000005", "email": "luis5@gmail.com"},
                        {"id_contacto": 6, "nombre": "Sofía Hernández", "telefono": "5510000006", "email": "sofia6@gmail.com"},
                        {"id_contacto": 7, "nombre": "Miguel Flores", "telefono": "5510000007", "email": "miguel7@gmail.com"},
                        {"id_contacto": 8, "nombre": "Laura Gómez", "telefono": "5510000008", "email": "laura8@gmail.com"},
                        {"id_contacto": 9, "nombre": "Jorge Díaz", "telefono": "5510000009", "email": "jorge9@gmail.com"},
                        {"id_contacto": 10, "nombre": "Fernanda Ruiz", "telefono": "5510000010", "email": "fernanda10@gmail.com"}
                    ],
            "count":10,
            "message":"Datos consultados exitosamente",
            "datetime":"11/03/2026",
            "limit":10,
            "skip":0
        }
    assert response.status_code == 200
    assert response.json () == data

# 2. GET 202 /v1/contactos?limit=10&skip=90 ultimos 10 contacto
def test_get_contactos_limit_10_skip_90():
    response = client.get("/v1/contactos?limit=10&skip=90")
    assert response.status_code == 200

# 3. GET 400 /v1/contactos?limit=-10&skip=0 Error en limit
def test_get_contactos_limit_negativo_skip_0():
    response = client.get("/v1/contactos?limit=-10&skip=0")
    assert response.status_code == 400

# 4. GET 400 /v1/contactos?limit=10&skip=-10 Error en skip
def test_get_contactos_limit_10_skip_negativo():
    response = client.get("/v1/contactos?limit=10&skip=-10")
    assert response.status_code == 400

# 5. GET 202 /v1/contactos?limit=0&skip=0 vacio
def test_get_contactos_limit_0_skip_0():
    response = client.get("/v1/contactos?limit=0&skip=0")
    assert response.status_code == 200

# 6. GET 202 /v1/contactos?skip=0 Regresar los primeros 10 contactos por default
def test_get_contactos_skip_0():
    response = client.get("/v1/contactos?skip=0")
    assert response.status_code == 200

# 7. GET 202 /v1/contactos?limit=10 Regresar los primeros 10 contactos por default
def test_get_contactos_limit_10():
    response = client.get("/v1/contactos?limit=10")
    assert response.status_code == 200

# 8. GET 202 /v1/contactos Regresar los primeros 10 contactos por default
def test_get_contactos():
    response = client.get("/v1/contactos")
    assert response.status_code == 200

# 9. GET 400 /v1/contactos?limit=x&skip=100 Mensaje de Error en limit
def test_get_contactos_limit_x_skip_100():
    response = client.get("/v1/contactos?limit=x&skip=100")
    assert response.status_code in [400, 422] 

# 10. GET 400 /v1/contactos?limit=10&skip=x Mensaje de Error en skip
def test_get_contactos_limit_10_skip_x():
    response = client.get("/v1/contactos?limit=10&skip=x")
    assert response.status_code in [400, 422]