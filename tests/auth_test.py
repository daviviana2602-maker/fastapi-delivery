def test_criar_conta(api_client):
    response = api_client.post(
        "/auth/criar_conta",
        json={
            "nome": "Davi Test",
            "email": "davi@test.com",
            "senha": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "id" in data["data"]
    
    

def test_login(api_client):
    api_client.post(
        "/auth/criar_conta",
        json={
            "nome": "Davi Login",
            "email": "login@test.com",
            "senha": "123456"
        }
    )


    response = api_client.post(
        "/auth/login",
        json={
            "email": "login@test.com",
            "senha": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]
    assert data["data"]["token_type"] == "Bearer"
    
    
    
def test_login_senha_errada(api_client):
    api_client.post(
        "/auth/criar_conta",
        json={
            "nome": "Davi Error",
            "email": "error@test.com",
            "senha": "123456"
        }
    )

    response = api_client.post(
        "/auth/login",
        json={
            "email": "error@test.com",
            "senha": "errada"
        }
    )

    assert response.status_code == 400
    
    
    
def test_refresh_token(api_client):
    api_client.post(
        "/auth/criar_conta",
        json={
            "nome": "Davi Refresh",
            "email": "refresh@test.com",
            "senha": "123456"
        }
    )

    login_res = api_client.post(
        "/auth/login",
        json={
            "email": "refresh@test.com",
            "senha": "123456"
        }
    )

    refresh_token = login_res.json()["data"]["refresh_token"]

    # usa refresh
    response = api_client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data["data"]
    assert data["success"] is True
    
    

def test_usuario_duplicado(api_client):
    api_client.post(
        "/auth/criar_conta",
        json={
            "nome": "Davi",
            "email": "dup@test.com",
            "senha": "123456"
        }
    )

    response = api_client.post(
        "/auth/criar_conta",
        json={
            "nome": "Davi 2",
            "email": "dup@test.com",
            "senha": "123456"
        }
    )

    assert response.status_code == 400