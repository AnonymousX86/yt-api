# -*- coding: utf-8 -*-
from random import choice


_LOWERCASE = [*'qwertyuiopasdfghjklzxcvbnm']
_UPPER = list(map(lambda x: x.upper(), _LOWERCASE))
_LETTERS = _LOWERCASE + _UPPER
_PREFIX = 'TEST_'


def random_string(length: int) -> str:
    result = _PREFIX
    for _ in range(length - len(_PREFIX)):
        result += choice(_LETTERS)
    return result
