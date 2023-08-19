from random import randint
from uuid import uuid4

from .constants import INVITE_CODE_LENGTH_LIMIT as INVITE_LIMIT
from users.models import User


def get_random_uuid4_str(limit):
    """
    Limit не может быть больше длины uuid4 строки.
    Или все сломается.
    """
    raw_string = str(uuid4())
    last_index = len(raw_string) - limit
    start_index = randint(0, last_index)
    return raw_string[start_index:start_index+limit]


def get_unique_invite_code():
    while True:
        code = get_random_uuid4_str(INVITE_LIMIT)
        if not User.objects.filter(invite_code=code).exists():
            return code
