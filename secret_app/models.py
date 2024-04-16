from pydantic import BaseModel


class SecretOutput(BaseModel):
    secret_key: str


class SecretInput(BaseModel):
    secret: str
    passphrase: str


class SecretPayload(BaseModel):
    passphrase: str
