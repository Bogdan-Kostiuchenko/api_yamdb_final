import re

from django.core.exceptions import ValidationError

from api_yamdb.reviews.constans import NAME_MAX_LENGTH, EMAIL_MAX_LENGTH, ROLES


def check_role_exists(role):
    for role_ex in ROLES:
        if role_ex == role:
            return
    raise ValidationError(f'Неверная роль "{role}"')


def validate_username(username):
    pattern = r'^[\w\d.@+-]+$'

    if username == 'me':
        raise ValidationError(
            'Запрещено использовать username - me!'
        )
    if len(username) > NAME_MAX_LENGTH:
        raise ValidationError(
            f'Длина логина превышает допустимое значение '
            f'{NAME_MAX_LENGTH} символов.'
        )
    if re.search(pattern, username):
        return username
    else:
        raise ValidationError('Логин содержит недопустимые символы.')


def validate_email(email):
    """Проверка email."""
    if len(email) > EMAIL_MAX_LENGTH:
        raise ValidationError(
            'Email превышает допустимую длину, сократите количество символов.'
        )
    return email
