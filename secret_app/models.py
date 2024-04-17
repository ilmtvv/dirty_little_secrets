from pydantic import BaseModel


class SecretOutput(BaseModel):
    secret_key: str


class SecretInput(BaseModel):
    """
    tll_day it's Time To Live, expiration time
    """
    secret: str
    passphrase: str
    ttl_day: int


class SecretPayload(BaseModel):
    passphrase: str
