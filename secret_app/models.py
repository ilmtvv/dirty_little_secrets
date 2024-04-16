from typing import Optional

from pydantic import BaseModel


class SecretOutput(BaseModel):
    secret_key: str


class SecretInput(BaseModel):
    secret: str
    passphrase: str
    ttl: Optional[int] = 3600   # Time to live in seconds
