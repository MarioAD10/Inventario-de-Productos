PRODUCTO = {"nombre": "Teclado", "descripcion": "Mecanico", "precio": 45.50, "cantidad": 10}


def test_health(client):
    assert client.get("/health").status_code == 200


def test_health_db(client):
    respuesta = client.get("/health/db")
    assert respuesta.status_code == 200
    assert "PostgreSQL" in respuesta.json()["database"]


def test_crear_y_listar(client):
    creado = client.post("/productos", json=PRODUCTO)
    assert creado.status_code == 201
    assert creado.json()["id"] == 1

    lista = client.get("/productos")
    assert lista.status_code == 200
    assert len(lista.json()) == 1
    assert lista.json()[0]["nombre"] == "Teclado"


def test_leer_producto_inexistente(client):
    respuesta = client.get("/productos/999")
    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "Producto no encontrado"


def test_editar_producto(client):
    client.post("/productos", json=PRODUCTO)
    nuevo = {**PRODUCTO, "cantidad": 8}
    respuesta = client.put("/productos/1", json=nuevo)
    assert respuesta.status_code == 200
    assert respuesta.json()["cantidad"] == 8


def test_eliminar_producto(client):
    client.post("/productos", json=PRODUCTO)
    assert client.delete("/productos/1").status_code == 204
    assert client.get("/productos/1").status_code == 404


def test_precio_negativo_rechazado(client):
    respuesta = client.post("/productos", json={**PRODUCTO, "precio": -5})
    assert respuesta.status_code == 422


def test_nombre_vacio_rechazado(client):
    respuesta = client.post("/productos", json={**PRODUCTO, "nombre": ""})
    assert respuesta.status_code == 422