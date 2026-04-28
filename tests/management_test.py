def test_promover_usuario(api_client, admin_headers, clean_user):

    response = api_client.patch(
        "/management/promover_usuario",
        json={"usuario_a_sofrer_alteracao": clean_user},
        headers=admin_headers
    )

    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["id"] == clean_user



def test_rebaixar_usuario(api_client, admin_headers, clean_user):

    api_client.patch(
        "/management/promover_usuario",
        json={"usuario_a_sofrer_alteracao": clean_user},
        headers=admin_headers
    )

    response = api_client.patch(
        "/management/rebaixar_usuario",
        json={"usuario_a_sofrer_alteracao": clean_user},
        headers=admin_headers
    )

    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["id"] == clean_user


def test_desativar_usuario(api_client, admin_headers, clean_user):

    response = api_client.patch(
        "/management/desativar_usuario",
        json={"usuario_a_sofrer_alteracao": clean_user},
        headers=admin_headers
    )

    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["id"] == clean_user



def test_reativar_usuario(api_client, admin_headers, clean_user):

    api_client.patch(
        "/management/desativar_usuario",
        json={"usuario_a_sofrer_alteracao": clean_user},
        headers=admin_headers
    )

    response = api_client.patch(
        "/management/reativar_usuario",
        json={"usuario_a_sofrer_alteracao": clean_user},
        headers=admin_headers
    )

    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["id"] == clean_user