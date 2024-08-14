NAME_MAX_LENGTH = 150

CHAR_FIELD_MAX_LENGTH = 256
SLUG_FIELD_MAX_LENGTH = 25

MIN_SCORE = 1
MAX_SCORE = 10
MIN_YEAR_PUB = -32768  # Нижняя граница SmallIntegerField

EMAIL_MAX_LENGTH = 254

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

USERS_ROLES = [(USER, 'Пользователь'),
               (MODERATOR, 'Модератор'),
               (ADMIN, 'Администратор')]

ROLES = (ADMIN, MODERATOR, USER)
EMAIL_ADMIN = 'admin@mail.ru'

RESERVE_USERNAME = 'me'
