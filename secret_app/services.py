import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional

import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def get_hashed_passphrase(passphrase: str) -> str:
    return hashlib.sha256(passphrase.encode()).hexdigest()


async def save_secret(secret: str, hashed_passphrase: str, ttl: int) -> str:
    secret_key = hashlib.sha256(os.urandom(32)).hexdigest()
    expires_at = datetime.utcnow() + timedelta(seconds=ttl)

    await r.hset(secret_key, mapping={
        'secret': secret,
        'hashed_passphrase': hashed_passphrase,
        'expires_at': expires_at,
    })

    return secret_key


async def get_and_delete_secret(secret_key: str) -> Optional[str]:
    secret_data = r.hgetall(secret_key)
    if secret_data:
        await r.delete(secret_key)
        return secret_data['secret']

    return None
