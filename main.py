from fastapi import FastAPI, HTTPException

from secret_app.models import SecretOutput, SecretInput, SecretPayload
from secret_app.services import get_hashed_passphrase, save_secret, get_and_delete_secret


app = FastAPI()     # app for manager of secrets


@app.post('/generate', response_model=SecretOutput)
def generate_secret(secret_input: SecretInput):
    """
    url for generate secret
    :param secret_input:
    :return: secret_key_json
    """
    hashed_passphrase = get_hashed_passphrase(secret_input.passphrase)
    secret_key = save_secret(secret_input.secret, hashed_passphrase, secret_input.ttl_day)
    return {'secret_key': secret_key}


@app.post('/secrets/{secret_key}', response_model=SecretPayload)
async def get_secret(secret_key: str):
    """
    url for get secret
    :param secret_key:
    :return:
    """
    secret = get_and_delete_secret(secret_key)
    if secret is None:
        raise HTTPException(status_code=404, detail='Secret not found or passphrase incorrect')
    return {'passphrase': secret}
