import hashlib
import os
from typing import Optional

import redis
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(host=os.getenv('HOST'), port=os.getenv('PORT'), decode_responses=True)


def get_hashed_passphrase(passphrase: str) -> str:
    """
    create hash
    :param passphrase:
    :return: hash
    """
    return hashlib.sha256(passphrase.encode()).hexdigest()


def save_secret(secret: str, hashed_passphrase: str, tll: int) -> str:
    """
    save secret in db
    :param secret:
    :param hashed_passphrase:
    :param tll:
    :return: secret_key:
    """
    secret_key = hashlib.sha256(os.urandom(32)).hexdigest()

    r.hset(secret_key, mapping={
        'secret': secret,
        'hashed_passphrase': hashed_passphrase,
        'tll': tll * 3600 * 24,
    })

    r.expire(secret_key, tll)

    return secret_key


def get_and_delete_secret(secret_key: str) -> Optional[str]:
    """
    get and delete secret
    :param secret_key:
    :return: secret
    """
    secret_data = r.hgetall(secret_key)
    if secret_data == {}:
        return None
    r.delete(secret_key)
    return secret_data['secret']
