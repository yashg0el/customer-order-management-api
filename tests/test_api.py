def test_customer_crud(client):
    response = client.post("/customers", json={
        "name": "Asha Sharma", "email": "asha@example.com", "phone": "9876543210"
    })
    assert response.status_code == 201
    customer_id = response.json()["id"]

    assert client.get(f"/customers/{customer_id}").status_code == 200
    updated = client.patch(f"/customers/{customer_id}", json={"name": "Asha S."})
    assert updated.status_code == 200
    assert updated.json()["name"] == "Asha S."

    assert client.delete(f"/customers/{customer_id}").status_code == 204
    assert client.get(f"/customers/{customer_id}").status_code == 404

def test_duplicate_email_returns_conflict(client):
    payload = {"name": "Asha Sharma", "email": "asha@example.com"}
    assert client.post("/customers", json=payload).status_code == 201
    assert client.post("/customers", json=payload).status_code == 409

def test_validation_rejects_invalid_customer(client):
    response = client.post("/customers", json={"name": "A", "email": "not-an-email"})
    assert response.status_code == 422

def test_product_create_and_order_reduces_stock(client):
    customer = client.post("/customers", json={
        "name": "Ravi Kumar", "email": "ravi@example.com"
    }).json()
    product = client.post("/products", json={
        "name": "Wireless Mouse", "sku": "MOUSE-001", "price": "799.00", "stock": 10
    })
    assert product.status_code == 201
    product_id = product.json()["id"]

    order = client.post("/orders", json={
        "customer_id": customer["id"], "product_id": product_id, "quantity": 3
    })
    assert order.status_code == 201
    assert client.get(f"/products/{product_id}").json()["stock"] == 7

def test_order_rejects_insufficient_stock(client):
    customer = client.post("/customers", json={
        "name": "Ravi Kumar", "email": "ravi@example.com"
    }).json()
    product = client.post("/products", json={
        "name": "Keyboard", "sku": "KEY-001", "price": "1200.00", "stock": 1
    }).json()
    response = client.post("/orders", json={
        "customer_id": customer["id"], "product_id": product["id"], "quantity": 2
    })
    assert response.status_code == 409
