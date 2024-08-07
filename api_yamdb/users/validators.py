
import re
from django.core.exceptions import ValidationError
from users.constans import EMAIL_MAX_LENGTH, NAME_MAX_LENGTH, USERS_ROLES


# def get_role_max_length():
#     """Длина поля роли."""
#     return max(len(role[0]) for role in USERS_ROLES.choices)


def validate_username(username):
    """Проверка логина."""
    if username.lower() == 'me':
        raise ValidationError(
            'Нельзя назвать логин "me".'
        )
    if len(username) > NAME_MAX_LENGTH:
        raise ValidationError(
            f'Длина логина не должна превышать '
            f'{NAME_MAX_LENGTH} символов.'
        )
    if not re.fullmatch(r'^[\w\d\.@+-]+$', username):
        raise ValidationError(
            'Логин содержит недопустимые символы.'
        )
    return username


def validate_email(email):
    """Проверка email."""
    if len(email) > EMAIL_MAX_LENGTH:
        raise ValidationError(
            'Email слишком длинный.'
        )
    return email
