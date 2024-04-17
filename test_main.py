from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_secret():
    data = {
        'secret': 'test',
        'pass_phrase': 'test',
        'tll': 2
    }

    # test for create secret #
    response_create_secret = client.post('/generate/', json=data)
    assert response_create_secret.status_code == 200

    data = {
        'pass_phrase': 'test',
    }
    # test for get secret #
    response_get_secret = client.post(f'/secrets/{response_create_secret.json()["secret_key"]}', json=data)
    assert response_get_secret.status_code == 200

    # test for get after get secret #
    response_get_secret = client.post(f'/secrets/{response_create_secret.json()["secret_key"]}', json=data)
    assert response_get_secret.status_code == 404
