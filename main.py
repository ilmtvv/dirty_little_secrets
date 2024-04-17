from fastapi import FastAPI, HTTPException

from secret_app.models import SecretKeyOutput, SecretInput, SecretOutput, PassPhraseInput
from secret_app.services import save_secret, get_and_delete_secret


app = FastAPI()     # app for manager of secrets


@app.post('/generate', response_model=SecretKeyOutput)
def generate_secret(secret_input: SecretInput):
    """
    url for generate secret
    :param secret_input:
    :return: secret_key_json
    """
    secret_key = save_secret(secret_input.secret, secret_input.pass_phrase, secret_input.ttl_day)
    return {'secret_key': secret_key}


@app.post('/secrets/{secret_key}', response_model=SecretOutput)
async def get_secret(secret_phrase: PassPhraseInput, secret_key: str):
    """
    url for get secret
    :param secret_phrase:
    :param secret_key:
    :return:
    """
    secret = get_and_delete_secret(secret_key, secret_phrase.pass_phrase)
    if secret is None:
        raise HTTPException(status_code=404, detail='Secret not found or passphrase incorrect')
    return {'secret': secret}
