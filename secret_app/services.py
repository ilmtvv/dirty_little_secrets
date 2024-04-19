import hashlib
import os
from typing import Optional

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

    r.hset(secret_key, mapping={
        'secret': secret,
        'passphrase': pass_phrase,
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
    if secret_data == {} or secret_data['passphrase'] != pass_phrase:
        return None
    r.delete(secret_key)
    return secret_data['secret']
