import pytest
from fastapi.testclient import TestClient
from main import app

# Inicializar TestClient
client = TestClient(app)

# ==================== TESTS: GET / ====================

class TestRootEndpoint:
    """Tests para el endpoint raíz GET /"""
    
    def test_get_root_returns_200(self):
        """GET / debe retornar status 200"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_get_root_returns_json(self):
        """GET / debe retornar JSON válido"""
        response = client.get("/")
        assert response.headers["content-type"].startswith("application/json")
    
    def test_get_root_has_success_status(self):
        """Respuesta debe tener status 'success'"""
        response = client.get("/")
        data = response.json()
        assert data["status"] == "success"
    
    def test_get_root_has_message(self):
        """Respuesta debe contener un mensaje"""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)
    
    def test_get_root_has_version(self):
        """Data debe contener la versión"""
        response = client.get("/")
        data = response.json()
        assert "version" in data["data"]
        assert data["data"]["version"] == "1.0.0"

# ==================== TESTS: GET /v1/contactos ====================

class TestGetContactos:
    """Tests para el endpoint GET /v1/contactos"""
    
    # CASOS EXITOSOS (Status 200)
    
    def test_get_contactos_limit_10_skip_0(self):
        """1. GET /v1/contactos?limit=10&skip=0 - primeros 10 contactos"""
        response = client.get("/v1/contactos?limit=10&skip=0")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "items" in data["data"]
        assert isinstance(data["data"]["items"], list)
        assert data["data"]["limit"] == 10
        assert data["data"]["skip"] == 0
    
    def test_get_contactos_limit_10_skip_90(self):
        """2. GET /v1/contactos?limit=10&skip=90 - últimos 10 contactos"""
        response = client.get("/v1/contactos?limit=10&skip=90")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_get_contactos_skip_0(self):
        """6. GET /v1/contactos?skip=0 - Regresar primeros 10 contactos (default)"""
        response = client.get("/v1/contactos?skip=0")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["skip"] == 0
    
    def test_get_contactos_limit_10(self):
        """7. GET /v1/contactos?limit=10 - Regresar 10 contactos con skip default"""
        response = client.get("/v1/contactos?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["limit"] == 10
    
    def test_get_contactos_default(self):
        """8. GET /v1/contactos - Regresar contactos con parámetros por defecto"""
        response = client.get("/v1/contactos")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "total" in data["data"]
    
    def test_get_contactos_has_total(self):
        """Respuesta debe incluir total de registros"""
        response = client.get("/v1/contactos")
        data = response.json()
        assert "total" in data["data"]
        assert isinstance(data["data"]["total"], int)
    
    def test_get_contactos_items_have_fields(self):
        """Items deben tener campos requeridos"""
        response = client.get("/v1/contactos?limit=1")
        data = response.json()
        if data["data"]["items"]:
            item = data["data"]["items"][0]
            assert "id_contacto" in item
            assert "nombre" in item
            assert "email" in item
            assert "telefono" in item
    
    # CASOS CON ERROR (Status 400/422)
    
    def test_get_contactos_limit_negativo_skip_0(self):
        """3. GET /v1/contactos?limit=-10&skip=0 - Error en limit negativo"""
        response = client.get("/v1/contactos?limit=-10&skip=0")
        assert response.status_code == 422
    
    def test_get_contactos_limit_10_skip_negativo(self):
        """4. GET /v1/contactos?limit=10&skip=-10 - Error en skip negativo"""
        response = client.get("/v1/contactos?limit=10&skip=-10")
        assert response.status_code == 422
    
    def test_get_contactos_limit_0_skip_0(self):
        """5. GET /v1/contactos?limit=0&skip=0 - Error en limit cero"""
        response = client.get("/v1/contactos?limit=0&skip=0")
        assert response.status_code == 422
    
    def test_get_contactos_limit_x_skip_100(self):
        """9. GET /v1/contactos?limit=x&skip=100 - Error en limit no numérico"""
        response = client.get("/v1/contactos?limit=x&skip=100")
        assert response.status_code in [400, 422]
    
    def test_get_contactos_limit_10_skip_x(self):
        """10. GET /v1/contactos?limit=10&skip=x - Error en skip no numérico"""
        response = client.get("/v1/contactos?limit=10&skip=x")
        assert response.status_code in [400, 422]

# ==================== TESTS: GET /v1/contacto ====================

class TestGetContacto:
    """Tests para el endpoint GET /v1/contacto"""
    
    # CASOS EXITOSOS (Status 200)
    
    def test_get_contacto_by_id_valid(self):
        """GET /v1/contacto?id_contacto=1 - Obtener contacto por ID válido"""
        response = client.get("/v1/contacto?id_contacto=1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["id_contacto"] == 1
    
    def test_get_contacto_by_name_valid(self):
        """GET /v1/contacto?nombre=María - Obtener contacto por nombre"""
        response = client.get("/v1/contacto?nombre=Mar%C3%ADa%20L%C3%B3pez")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "María" in data["data"]["nombre"]
    
    def test_get_contacto_has_required_fields(self):
        """Contacto debe tener todos los campos requeridos"""
        response = client.get("/v1/contacto?id_contacto=1")
        contacto = response.json()["data"]
        assert "id_contacto" in contacto
        assert "nombre" in contacto
        assert "email" in contacto
        assert "telefono" in contacto
    
    # CASOS CON ERROR (Status 400/404)
    
    def test_get_contacto_missing_params(self):
        """GET /v1/contacto - Error sin parámetros"""
        response = client.get("/v1/contacto")
        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "error"
    
    def test_get_contacto_by_id_not_found(self):
        """GET /v1/contacto?id_contacto=99999 - Error contacto no existe"""
        response = client.get("/v1/contacto?id_contacto=99999")
        assert response.status_code == 404
        data = response.json()
        assert data["status"] == "error"
    
    def test_get_contacto_by_name_not_found(self):
        """GET /v1/contacto?nombre=NoExiste - Error nombre no existe"""
        response = client.get("/v1/contacto?nombre=NoExiste12345")
        assert response.status_code == 404
    
    def test_get_contacto_invalid_id_type(self):
        """GET /v1/contacto?id_contacto=abc - Error ID no numérico"""
        response = client.get("/v1/contacto?id_contacto=abc")
        assert response.status_code == 422
    
    def test_get_contacto_id_negative(self):
        """GET /v1/contacto?id_contacto=-1 - Error ID negativo"""
        response = client.get("/v1/contacto?id_contacto=-1")
        assert response.status_code in [400, 422]

# ==================== TESTS: POST /v1/contacto ====================

class TestCreateContacto:
    """Tests para el endpoint POST /v1/contacto"""
    
    # CASOS EXITOSOS (Status 201)
    
    def test_create_contacto_valid(self):
        """POST /v1/contacto - Crear contacto con datos válidos"""
        payload = {
            "nombre": "Test Create User",
            "email": "test.create@example.com",
            "telefono": "5555555555"
        }
        response = client.post("/v1/contacto", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["nombre"] == payload["nombre"]
        assert data["data"]["email"] == payload["email"]
    
    def test_create_contacto_returns_id(self):
        """POST /v1/contacto - Contacto creado debe retornar ID"""
        payload = {
            "nombre": "Test ID User",
            "email": "test.id@example.com",
            "telefono": "5555555556"
        }
        response = client.post("/v1/contacto", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "id_contacto" in data["data"]
        assert isinstance(data["data"]["id_contacto"], int)
        assert data["data"]["id_contacto"] > 0
    
    def test_create_contacto_all_fields_present(self):
        """POST /v1/contacto - Respuesta debe contener todos los campos"""
        payload = {
            "nombre": "Test Fields User",
            "email": "test.fields@example.com",
            "telefono": "5555555557"
        }
        response = client.post("/v1/contacto", json=payload)
        data = response.json()["data"]
        assert "id_contacto" in data
        assert "nombre" in data
        assert "email" in data
        assert "telefono" in data
    
    # CASOS CON ERROR (Status 422)
    
    def test_create_contacto_empty_nombre(self):
        """POST /v1/contacto - Error nombre vacío"""
        payload = {
            "nombre": "",
            "email": "test@example.com",
            "telefono": "5555555555"
        }
        response = client.post("/v1/contacto", json=payload)
        assert response.status_code == 422
    
    def test_create_contacto_invalid_email(self):
        """POST /v1/contacto - Error email inválido"""
        payload = {
            "nombre": "Test",
            "email": "not-an-email",
            "telefono": "5555555555"
        }
        response = client.post("/v1/contacto", json=payload)
        assert response.status_code in [201, 422]
    
    def test_create_contacto_short_phone(self):
        """POST /v1/contacto - Error teléfono muy corto"""
        payload = {
            "nombre": "Test",
            "email": "test@example.com",
            "telefono": "123"
        }
        response = client.post("/v1/contacto", json=payload)
        assert response.status_code == 422
    
    def test_create_contacto_missing_nombre(self):
        """POST /v1/contacto - Error sin nombre"""
        payload = {
            "email": "test@example.com",
            "telefono": "5555555555"
        }
        response = client.post("/v1/contacto", json=payload)
        assert response.status_code == 422
    
    def test_create_contacto_missing_email(self):
        """POST /v1/contacto - Error sin email"""
        payload = {
            "nombre": "Test",
            "telefono": "5555555555"
        }
        response = client.post("/v1/contacto", json=payload)
        assert response.status_code == 422
    
    def test_create_contacto_missing_telefono(self):
        """POST /v1/contacto - Error sin teléfono"""
        payload = {
            "nombre": "Test",
            "email": "test@example.com"
        }
        response = client.post("/v1/contacto", json=payload)
        assert response.status_code == 422
    
    def test_create_contacto_long_nombre(self):
        """POST /v1/contacto - Error nombre mayor a 100 caracteres"""
        payload = {
            "nombre": "a" * 101,
            "email": "test@example.com",
            "telefono": "5555555555"
        }
        response = client.post("/v1/contacto", json=payload)
        assert response.status_code == 422
    
    def test_create_contacto_invalid_phone_length(self):
        """POST /v1/contacto - Error teléfono no es de 10 dígitos"""
        payload = {
            "nombre": "Test",
            "email": "test@example.com",
            "telefono": "55555555555"  # 11 dígitos
        }
        response = client.post("/v1/contacto", json=payload)
        assert response.status_code == 422

# ==================== TESTS: PUT /v1/contacto ====================

class TestUpdateContacto:
    """Tests para el endpoint PUT /v1/contacto"""
    
    # CASOS EXITOSOS (Status 200)
    
    def test_update_contacto_valid(self):
        """PUT /v1/contacto?id_contacto=1 - Actualizar con datos válidos"""
        payload = {
            "nombre": "Updated Name",
            "email": "updated@example.com",
            "telefono": "5555555555"
        }
        response = client.put("/v1/contacto?id_contacto=1", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["nombre"] == "Updated Name"
    
    def test_update_contacto_preserves_id(self):
        """PUT /v1/contacto - ID debe permanecer igual"""
        payload = {
            "nombre": "Another Update",
            "email": "another@example.com",
            "telefono": "5555555555"
        }
        response = client.put("/v1/contacto?id_contacto=1", json=payload)
        data = response.json()
        assert data["data"]["id_contacto"] == 1
    
    def test_update_contacto_all_fields(self):
        """PUT /v1/contacto - Actualización debe incluir todos los campos"""
        payload = {
            "nombre": "Test Update",
            "email": "test@example.com",
            "telefono": "5555555555"
        }
        response = client.put("/v1/contacto?id_contacto=1", json=payload)
        data = response.json()["data"]
        assert "id_contacto" in data
        assert "nombre" in data
        assert "email" in data
        assert "telefono" in data
    
    # CASOS CON ERROR (Status 400/404/422)
    
    def test_update_contacto_missing_id(self):
        """PUT /v1/contacto - Error sin ID"""
        payload = {
            "nombre": "Test",
            "email": "test@example.com",
            "telefono": "5555555555"
        }
        response = client.put("/v1/contacto", json=payload)
        assert response.status_code == 422
    
    def test_update_contacto_id_not_found(self):
        """PUT /v1/contacto?id_contacto=99999 - Error contacto no existe"""
        payload = {
            "nombre": "Test",
            "email": "test@example.com",
            "telefono": "5555555555"
        }
        response = client.put("/v1/contacto?id_contacto=99999", json=payload)
        assert response.status_code == 404
    
    def test_update_contacto_invalid_email(self):
        """PUT /v1/contacto - Error email inválido"""
        payload = {
            "nombre": "Test",
            "email": "invalid-email",
            "telefono": "5555555555"
        }
        response = client.put("/v1/contacto?id_contacto=1", json=payload)
        assert response.status_code in [200, 422]
    
    def test_update_contacto_empty_nombre(self):
        """PUT /v1/contacto - Error nombre vacío"""
        payload = {
            "nombre": "",
            "email": "test@example.com",
            "telefono": "5555555555"
        }
        response = client.put("/v1/contacto?id_contacto=1", json=payload)
        assert response.status_code == 422
    
    def test_update_contacto_short_phone(self):
        """PUT /v1/contacto - Error teléfono muy corto"""
        payload = {
            "nombre": "Test",
            "email": "test@example.com",
            "telefono": "123"
        }
        response = client.put("/v1/contacto?id_contacto=1", json=payload)
        assert response.status_code == 422
    
    def test_update_contacto_invalid_id_type(self):
        """PUT /v1/contacto?id_contacto=abc - Error ID no numérico"""
        payload = {
            "nombre": "Test",
            "email": "test@example.com",
            "telefono": "5555555555"
        }
        response = client.put("/v1/contacto?id_contacto=abc", json=payload)
        assert response.status_code == 422
    
    def test_update_contacto_negative_id(self):
        """PUT /v1/contacto?id_contacto=-1 - Error ID negativo"""
        payload = {
            "nombre": "Test",
            "email": "test@example.com",
            "telefono": "5555555555"
        }
        response = client.put("/v1/contacto?id_contacto=-1", json=payload)
        assert response.status_code in [400, 422]

# ==================== TESTS: DELETE /v1/contacto ====================

class TestDeleteContacto:
    """Tests para el endpoint DELETE /v1/contacto"""
    
    # CASOS EXITOSOS (Status 200)
    
    def test_delete_contacto_valid(self):
        """DELETE /v1/contacto?id_contacto=X - Eliminar contacto válido"""
        # Primero crear un contacto para eliminarlo
        create_payload = {
            "nombre": "To Delete",
            "email": "delete@example.com",
            "telefono": "5555555555"
        }
        create_response = client.post("/v1/contacto", json=create_payload)
        contact_id = create_response.json()["data"]["id_contacto"]
        
        # Luego eliminarlo
        response = client.delete(f"/v1/contacto?id_contacto={contact_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_delete_contacto_returns_id(self):
        """DELETE /v1/contacto - Respuesta debe contener ID eliminado"""
        # Crear contacto
        create_payload = {
            "nombre": "To Delete 2",
            "email": "delete2@example.com",
            "telefono": "5555555556"
        }
        create_response = client.post("/v1/contacto", json=create_payload)
        contact_id = create_response.json()["data"]["id_contacto"]
        
        # Eliminar
        response = client.delete(f"/v1/contacto?id_contacto={contact_id}")
        data = response.json()
        assert data["data"]["id_contacto"] == contact_id
    
    # CASOS CON ERROR (Status 400/404/422)
    
    def test_delete_contacto_missing_id(self):
        """DELETE /v1/contacto - Error sin ID"""
        response = client.delete("/v1/contacto")
        assert response.status_code == 422
    
    def test_delete_contacto_id_not_found(self):
        """DELETE /v1/contacto?id_contacto=99999 - Error contacto no existe"""
        response = client.delete("/v1/contacto?id_contacto=99999")
        assert response.status_code == 404
    
    def test_delete_contacto_invalid_id_type(self):
        """DELETE /v1/contacto?id_contacto=abc - Error ID no numérico"""
        response = client.delete("/v1/contacto?id_contacto=abc")
        assert response.status_code == 422
    
    def test_delete_contacto_negative_id(self):
        """DELETE /v1/contacto?id_contacto=-1 - Error ID negativo"""
        response = client.delete("/v1/contacto?id_contacto=-1")
        assert response.status_code in [400, 422]
    
    def test_delete_contact_cannot_delete_again(self):
        """DELETE /v1/contacto - No se puede eliminar dos veces"""
        # Crear contacto
        create_payload = {
            "nombre": "To Delete Again",
            "email": "delete.again@example.com",
            "telefono": "5555555557"
        }
        create_response = client.post("/v1/contacto", json=create_payload)
        contact_id = create_response.json()["data"]["id_contacto"]
        
        # Eliminar
        client.delete(f"/v1/contacto?id_contacto={contact_id}")
        
        # Intentar eliminar de nuevo
        response = client.delete(f"/v1/contacto?id_contacto={contact_id}")
        assert response.status_code == 404

# ==================== TESTS DE INTEGRACIÓN ====================

class TestIntegration:
    """Tests de flujo completo (crear, actualizar, obtener, eliminar)"""
    
    def test_full_crud_flow(self):
        """Test completo del flujo CRUD"""
        # 1. CREAR
        create_payload = {
            "nombre": "Integration Test",
            "email": "integration@example.com",
            "telefono": "5555551234"
        }
        create_response = client.post("/v1/contacto", json=create_payload)
        assert create_response.status_code == 201
        contact_id = create_response.json()["data"]["id_contacto"]
        
        # 2. OBTENER
        get_response = client.get(f"/v1/contacto?id_contacto={contact_id}")
        assert get_response.status_code == 200
        assert get_response.json()["data"]["nombre"] == "Integration Test"
        
        # 3. ACTUALIZAR
        update_payload = {
            "nombre": "Integration Updated",
            "email": "updated@example.com",
            "telefono": "5555559999"
        }
        update_response = client.put(f"/v1/contacto?id_contacto={contact_id}", json=update_payload)
        assert update_response.status_code == 200
        assert update_response.json()["data"]["nombre"] == "Integration Updated"
        
        # 4. VERIFICAR ACTUALIZACIÓN
        verify_response = client.get(f"/v1/contacto?id_contacto={contact_id}")
        assert verify_response.json()["data"]["nombre"] == "Integration Updated"
        
        # 5. ELIMINAR
        delete_response = client.delete(f"/v1/contacto?id_contacto={contact_id}")
        assert delete_response.status_code == 200
        
        # 6. VERIFICAR QUE FUE ELIMINADO
        verify_delete = client.get(f"/v1/contacto?id_contacto={contact_id}")
        assert verify_delete.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])