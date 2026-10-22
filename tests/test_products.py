
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Product API is running"}


def test_create_product(client, auth_headers):
    response = client.post(
        "/products",
        json={
            "name": "Notebook",
            "price": 120,
            "description": "A ruled notebook",
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Notebook"
    assert data["price"] == 120
    assert data["description"] == "A ruled notebook"
    assert isinstance(data["id"], int)


def test_list_products(client, auth_headers):
    client.post(
        "/products",
        json={
            "name": "Notebook",
            "price": 120,
            "description": "Ruled pages",
        },
        headers=auth_headers,
    )

    response = client.get("/products")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Notebook"


def test_update_product(client, auth_headers):
    created = client.post(
        "/products",
        json={"name": "Notebook", "price": 120},
        headers=auth_headers,
    )
    assert created.status_code == 201

    product_id = created.json()["id"]

    response = client.patch(
        f"/products/{product_id}",
        json={"description": "Updated description"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["description"] == "Updated description"


def test_get_missing_product(client):
    response = client.get("/products/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_reject_invalid_price(client, auth_headers):
    response = client.post(
        "/products",
        json={"name": "Notebook", "price": -10},
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_delete_product(client, auth_headers):
    created = client.post(
        "/products",
        json={"name": "Notebook", "price": 120},
        headers=auth_headers,
    )
    assert created.status_code == 201

    product_id = created.json()["id"]

    response = client.delete(
        f"/products/{product_id}",
        headers=auth_headers,
    )

    assert response.status_code == 204

    check = client.get(f"/products/{product_id}")
    assert check.status_code == 404


def test_create_product_without_token_returns_401(client):
    response = client.post(
        "/products",
        json={"name": "Notebook", "price": 120},
    )

    assert response.status_code == 401
