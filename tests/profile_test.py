def test_editar_nome(api_client):
    api_client.post(
        "/auth/criar_conta",
        json={
            "nome": "Davi",
            "email": "davi@test.com",
            "senha": "123456"
        }
    )

    # login para pegar token
    login = api_client.post(
        "/auth/login",
        json={
            "email": "davi@test.com",
            "senha": "123456"
        }
    )

    token = login.json()["data"]["access_token"]

    # atualiza nome
    response = api_client.patch(
        "/profile/editar_perfil",
        json={
            "nome": "Davi Atualizado"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["nome"] == "Davi Atualizado"
    
    
    
def test_editar_email_com_sucesso(api_client):
    api_client.post(
        "/auth/criar_conta",
        json={
            "nome": "Davi",
            "email": "davi@test.com",
            "senha": "123456"
        }
    )

    login = api_client.post(
        "/auth/login",
        json={
            "email": "davi@test.com",
            "senha": "123456"
        }
    )

    token = login.json()["data"]["access_token"]

    response = api_client.patch(
        "/profile/editar_perfil",
        json={
            "email": "novo@test.com",
            "senha_atual": "123456"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["data"]["email"] == "novo@test.com"
    
    
    
def test_editar_email_sem_senha_atual(api_client):
    api_client.post(
        "/auth/criar_conta",
        json={
            "nome": "Davi",
            "email": "davi@test.com",
            "senha": "123456"
        }
    )

    login = api_client.post(
        "/auth/login",
        json={
            "email": "davi@test.com",
            "senha": "123456"
        }
    )

    token = login.json()["data"]["access_token"]

    response = api_client.patch(
        "/profile/editar_perfil",
        json={
            "email": "novo@test.com"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    
    
    
def test_editar_senha_atual_errada(api_client):
    api_client.post(
        "/auth/criar_conta",
        json={
            "nome": "Davi",
            "email": "davi@test.com",
            "senha": "123456"
        }
    )

    login = api_client.post(
        "/auth/login",
        json={
            "email": "davi@test.com",
            "senha": "123456"
        }
    )

    token = login.json()["data"]["access_token"]

    response = api_client.patch(
        "/profile/editar_perfil",
        json={
            "email": "novo@test.com",
            "senha_atual": "errada"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    
    

def test_excluir_usuario(api_client):
    api_client.post(
        "/auth/criar_conta",
        json={
            "nome": "Davi",
            "email": "davi@test.com",
            "senha": "123456"
        }
    )

    login = api_client.post(
        "/auth/login",
        json={
            "email": "davi@test.com",
            "senha": "123456"
        }
    )

    token = login.json()["data"]["access_token"]

    response = api_client.request(
    "DELETE",
    "/profile/excluir_conta?senha_atual=123456",
    headers={"Authorization": f"Bearer {token}"}
)
    

    assert response.status_code == 200
    assert response.json()["success"] is True
    
    
    
def test_excluir_usuario_senha_errada(api_client):
    api_client.post(
        "/auth/criar_conta",
        json={
            "nome": "Davi",
            "email": "davi@excluirerrado.com",
            "senha": "123456"
        }
    )

    login = api_client.post(
        "/auth/login",
        json={
            "email": "davi@excluirerrado.com",
            "senha": "123456"
        }
    )

    token = login.json()["data"]["access_token"]

    response = api_client.request(
    "DELETE",
    "/profile/excluir_conta?senha_atual=errada",
    headers={"Authorization": f"Bearer {token}"}
)

    assert response.status_code == 400
    
    
    
def test_excluir_usuario_com_pedido_pendente(api_client):
    api_client.post(
    "/auth/criar_conta",
    json={
        "nome": "Davi",
        "email": "pendente@test.com",
        "senha": "123456"
    }
)

    login = api_client.post(
    "/auth/login",
    json={
        "email": "pendente@test.com",
        "senha": "123456"
    }
    )

    token = login.json()["data"]["access_token"]

    # simular pedido pendente
    api_client.post(
        "/order/pedido",
        headers={"Authorization": f"Bearer {token}"}
    )

    # tentar excluir
    response = api_client.request(
    "DELETE",
    "/profile/excluir_conta?senha_atual=123456",
    headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400