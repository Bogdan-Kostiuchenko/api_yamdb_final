import re

from django.core.exceptions import ValidationError

from reviews.constans import RESERVE_USERNAME


def validate_username(username):
    pattern = r'^[\w.@+-]+\Z'

    if username == RESERVE_USERNAME:
        raise ValidationError(
            f'Запрещено использовать username - {RESERVE_USERNAME}!'
        )

    if not re.match(pattern, username):
        forbidden_characters = re.findall(pattern, username)
        raise ValidationError(f'Логин содержит недопустимые символы: '
                              f'{forbidden_characters}')
    return username
