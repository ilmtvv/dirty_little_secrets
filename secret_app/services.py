import hashlib
import os
from typing import Optional

import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def get_hashed_passphrase(passphrase: str) -> str:
    return hashlib.sha256(passphrase.encode()).hexdigest()


def save_secret(secret: str, hashed_passphrase: str) -> str:
    secret_key = hashlib.sha256(os.urandom(32)).hexdigest()

    r.hset(secret_key, mapping={
        'secret': secret,
        'hashed_passphrase': hashed_passphrase,
    })

    return secret_key


def get_and_delete_secret(secret_key: str) -> Optional[str]:
    secret_data = r.hgetall(secret_key)
    if secret_data == {}:
        return None
    r.delete(secret_key)
    return secret_data['secret']
