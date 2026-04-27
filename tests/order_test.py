def test_criar_pedido(api_client):
    api_client.post("/auth/criar_conta", json={
        "nome": "User Order",
        "email": "order@test.com",
        "senha": "123456"
    })

    login = api_client.post("/auth/login", json={
        "email": "order@test.com",
        "senha": "123456"
    })

    token = login.json()["data"]["access_token"]

    response = api_client.post(
        "/order/pedido",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "PENDENTE"
    
    

def test_adicionar_item(api_client):
    api_client.post("/auth/criar_conta", json={
        "nome": "User Item",
        "email": "item@test.com",
        "senha": "123456"
    })

    login = api_client.post("/auth/login", json={
        "email": "item@test.com",
        "senha": "123456"
    })

    token = login.json()["data"]["access_token"]

    pedido = api_client.post(
        "/order/pedido",
        headers={"Authorization": f"Bearer {token}"}
    )

    pedido_id = pedido.json()["data"]["id"]

    response = api_client.post(
        "/order/pedido/adicionar_item",
        json={
            "pedido_id": pedido_id,
            "nome": "Arroz",
            "quantidade": 1,
            "tamanho": "tradicional"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    
    

def test_concluir_pedido(api_client):
    api_client.post("/auth/criar_conta", json={
        "nome": "User Finish",
        "email": "finish@test.com",
        "senha": "123456"
    })

    login = api_client.post("/auth/login", json={
        "email": "finish@test.com",
        "senha": "123456"
    })

    token = login.json()["data"]["access_token"]

    pedido = api_client.post(
        "/order/pedido",
        headers={"Authorization": f"Bearer {token}"}
    )

    pedido_id = pedido.json()["data"]["id"]


    api_client.post(
        "/order/pedido/adicionar_item",
        json={
            "pedido_id": pedido_id,
            "nome": "Bife",
            "quantidade": 3,
            "tamanho": "tradicional"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    
    response = api_client.patch(
        "/order/pedido/concluir",
        json={"pedido_id": pedido_id},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["data"]["preco"] >= 0
    
    
    
def test_cancelar_pedido(api_client):
    api_client.post("/auth/criar_conta", json={
        "nome": "User Cancel",
        "email": "cancel@test.com",
        "senha": "123456"
    })

    login = api_client.post("/auth/login", json={
        "email": "cancel@test.com",
        "senha": "123456"
    })

    token = login.json()["data"]["access_token"]

    pedido = api_client.post(
        "/order/pedido",
        headers={"Authorization": f"Bearer {token}"}
    )

    pedido_id = pedido.json()["data"]["id"]

    response = api_client.patch(
        "/order/pedido/cancelar",
        json={"pedido_id": pedido_id},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    
    

def test_ajustar_item(api_client):
    api_client.post("/auth/criar_conta", json={
        "nome": "User Adjust",
        "email": "adjust@test.com",
        "senha": "123456"
    })

    login = api_client.post("/auth/login", json={
        "email": "adjust@test.com",
        "senha": "123456"
    })

    token = login.json()["data"]["access_token"]

    pedido = api_client.post(
        "/order/pedido",
        headers={"Authorization": f"Bearer {token}"}
    )

    pedido_id = pedido.json()["data"]["id"]

    item = api_client.post(
        "/order/pedido/adicionar_item",
        json={
            "pedido_id": pedido_id,
            "nome": "Estrogonofe",
            "quantidade": 1,
            "tamanho": "tradicional"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    item_id = item.json()["data"]["id"]

    response = api_client.patch(
        "/order/pedido/item",
        json={
            "item_id": item_id,
            "ajuste": 5
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    
    

def test_listar_pedido_temp(api_client):
    api_client.post("/auth/criar_conta", json={
        "nome": "User List",
        "email": "list@test.com",
        "senha": "123456"
    })

    login = api_client.post("/auth/login", json={
        "email": "list@test.com",
        "senha": "123456"
    })

    token = login.json()["data"]["access_token"]

    pedido = api_client.post(
        "/order/pedido",
        headers={"Authorization": f"Bearer {token}"}
    )

    pedido_id = pedido.json()["data"]["id"]

    api_client.post(
        "/order/pedido/adicionar_item",
        json={
            "pedido_id": pedido_id,
            "nome": "Frango",
            "quantidade": 2,
            "tamanho": "grande"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    response = api_client.get(
        "/order/pedido/item/listar_pedido_temp",
        params={"pedido_id": pedido_id},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200