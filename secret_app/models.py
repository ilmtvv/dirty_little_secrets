from pydantic import BaseModel


class SecretKeyOutput(BaseModel):
    secret_key: str


class SecretInput(BaseModel):
    """
    tll_day it's Time To Live, expiration time, default=1
    """
    secret: str
    pass_phrase: str
    ttl_day: int = 1


class SecretOutput(BaseModel):
    secret: str


class PassPhraseInput(BaseModel):
    pass_phrase: str
