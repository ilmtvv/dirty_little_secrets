from pydantic import BaseModel


class SecretOutput(BaseModel):
    secret_key: str


class SecretInput(BaseModel):
    """
    tll_day it's Time To Live, expiration time, default=1
    """
    secret: str
    passphrase: str
    ttl_day: int = 1


class SecretPayload(BaseModel):
    passphrase: str
