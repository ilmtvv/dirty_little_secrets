from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_secret():
    data = {
        'secret': 'test',
        'passphrase': 'test',
        'tll': 2
    }

    # test for create secret #
    response_create_secret = client.post('/generate/', json=data)
    assert response_create_secret.status_code == 200

    # test for get secret #
    responce_get_secret = client.post(f'/secrets/{response_create_secret.json()["secret_key"]}')
    assert responce_get_secret.status_code == 200

    # test for get after get secret #
    responce_get_secret = client.post(f'/secrets/{response_create_secret.json()["secret_key"]}')
    assert responce_get_secret.status_code == 404
