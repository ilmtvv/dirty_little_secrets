from fastapi import FastAPI, HTTPException

from secret_app.models import SecretOutput, SecretInput
from secret_app.services import get_hashed_passphrase, save_secret, get_and_delete_secret

app = FastAPI()


@app.post('/generate', response_model=SecretOutput)
async def generate_secret(secret_input: SecretInput):
    hashed_passphrase = get_hashed_passphrase(secret_input.passphrase)
    secret_key = await save_secret(secret_input.secret, hashed_passphrase, secret_input.ttl)
    return {'secret_key': secret_key}


@app.post('/secrets/{secret_key}', response_model=SecretOutput)
async def get_secret(secret_key: str):
    secret = await get_and_delete_secret(secret_key)
    if secret is None:
        raise HTTPException(status_code=404, detail='Secret not found or passphrase incorrect')
    return {'secret': secret}
