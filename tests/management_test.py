def test_promover_usuario(api_client, admin_headers, user_alvo):

    response = api_client.patch(
        "/management/promover_usuario",
        json={"usuario_a_sofrer_alteracao": user_alvo},
        headers=admin_headers
    )

    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["id"] == user_alvo



def test_rebaixar_usuario(api_client, admin_headers, user_alvo):

    # garante estado: precisa ser admin antes de rebaixar
    api_client.patch(
        "/management/promover_usuario",
        json={"usuario_a_sofrer_alteracao": user_alvo},
        headers=admin_headers
    )

    response = api_client.patch(
        "/management/rebaixar_usuario",
        json={"usuario_a_sofrer_alteracao": user_alvo},
        headers=admin_headers
    )

    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["id"] == user_alvo



def test_desativar_usuario(api_client, admin_headers, user_alvo):

    response = api_client.patch(
        "/management/desativar_usuario",
        json={"usuario_a_sofrer_alteracao": user_alvo},
        headers=admin_headers
    )

    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["id"] == user_alvo



def test_reativar_usuario(api_client, admin_headers, user_alvo):

    # garante estado: precisa estar desativado antes
    api_client.patch(
        "/management/desativar_usuario",
        json={"usuario_a_sofrer_alteracao": user_alvo},
        headers=admin_headers
    )

    response = api_client.patch(
        "/management/reativar_usuario",
        json={"usuario_a_sofrer_alteracao": user_alvo},
        headers=admin_headers
    )

    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["id"] == user_alvo