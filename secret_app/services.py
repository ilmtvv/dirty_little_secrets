import hashlib
import os
from typing import Optional
from cryptography.fernet import Fernet

import redis
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(host=os.getenv('HOST'), port=os.getenv('PORT'), db=0, decode_responses=True)  # Snapshotting (RDB) on,
# auto-decode on and without password

# # connect to db with password and db #
# r = redis.Redis(host=os.getenv('HOST'), port=os.getenv('PORT'), password=None, db=os.getenv('DB'))
# r.config_set('requirepass', os.getenv('PASSWORD'))
# r.close()
#
# r = redis.Redis(host=os.getenv('HOST'), port=os.getenv('PORT'), password=os.getenv('PASSWORD'), decode_responses=True)
#
# try:
#     response = r.ping()
#     print(f"Connected to Redis: {response}")
# except redis.ConnectionError:
#     print("Failed to connect to Redis")


def save_secret(secret: str, pass_phrase: str, tll: int) -> str:
    """
    save secret in db
    :param secret:
    :param pass_phrase:
    :param tll:
    :return: secret_key:
    """
    secret_key = hashlib.sha256(os.urandom(32)).hexdigest()

    key = Fernet.generate_key()

    r.set(secret_key[::-1], key)
    r.hset(secret_key, mapping={
        'secret': Fernet(key).encrypt(secret.encode()),
        'pass_phrase': Fernet(key).encrypt(pass_phrase.encode()),
    })

    tll = tll * 3600 * 24
    r.expire(secret_key, tll)

    return secret_key


def get_and_delete_secret(secret_key: str, pass_phrase: str) -> Optional[str]:
    """
    get and delete secret
    :param pass_phrase:
    :param secret_key:
    :return: secret
    """
    secret_data = r.hgetall(secret_key)
    key = r.get(secret_key[::-1])

    if secret_data == {}:
        return None
    elif pass_phrase != Fernet(key).decrypt(secret_data['pass_phrase']).decode():
        return 'WRONG!'
    r.delete(secret_key)
    r.delete(secret_key[::-1])
    return Fernet(key).decrypt(secret_data['secret']).decode()
