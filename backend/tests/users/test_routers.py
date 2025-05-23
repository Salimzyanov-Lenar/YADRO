def test_health_check(client):
    response = client.get('/health/')
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}


def test_get_users_has_next(client, setup_and_teardown):
    response = client.get('/api/users/v1/?skip=0&limit=2')
    assert response.status_code == 200

    data = response.json()

    assert "users" in data
    assert "total_amount" in data
    assert "has_next" in data

    assert data["total_amount"] == 3
    assert len(data["users"]) == 2
    assert data["has_next"] is True


def test_get_users_has_not_next(client, setup_and_teardown):
    response = client.get('/api/users/v1/?skip=2&limit=2')
    assert response.status_code == 200

    data = response.json()

    assert data["total_amount"] == 3
    assert len(data["users"]) == 1
    assert data["has_next"] is False


def test_get_random_user(client, setup_and_teardown):
    response = client.get('/api/users/v1/random/')
    assert response.status_code == 200

    data  = response.json()

    assert "id" in data
    assert "first_name" in data
    assert "second_name" in data
    assert "phone_number" in data
    assert "email" in data
    assert "residing_place" in data
    assert "photo_url" in data


def test_get_user_by_id(client, setup_and_teardown):
    response = client.get('/api/users/v1/1/')
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["gender"] == "male"
    assert data["first_name"] == "Ivan"
    assert data["second_name"] == "Ivanov"
    assert data["phone_number"] == "1234567890"
    assert data["email"] == "ivan@example.com"
    assert data["residing_place"] == "Moscow"
    assert data["photo_url"] == "http://example.com/photo1.jpg"


def test_get_user_by_id_not_found(client, setup_and_teardown):
    response = client.get('/api/users/v1/404/')
    assert response.status_code == 404

    data = response.json()
    
    assert data["detail"] == "User not Found"