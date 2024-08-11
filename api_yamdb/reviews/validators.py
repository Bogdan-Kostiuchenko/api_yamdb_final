import re

from django.core.exceptions import ValidationError

from reviews.constans import RESERVE_USERNAME


def validate_username(username):
    pattern = r'^[\w.@+-]+\Z'

    if username == RESERVE_USERNAME:
        raise ValidationError(
            f'Запрещено использовать username - {RESERVE_USERNAME}!'
        )
    if re.search(pattern, username):
        return username
    else:
        raise ValidationError(f'Логин содержит недопустимые символы: '
                              f'{re.findall(pattern, username)}')
