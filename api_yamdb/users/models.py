from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models

MAX_LENGTH = 100


class YamdbUser(AbstractUser):

    USERS_ROLES = [('user', 'Пользователь'),
                   ('moderator', 'Модератор'),
                   ('admin', 'Администратор')]

    username = models.SlugField('Имя пользователя',
                                max_length=MAX_LENGTH,
                                blank=False,
                                unique=True)
    email = models.EmailField('Электронная почта', unique=True)
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField('Код рeгистрации',
                                         max_length=MAX_LENGTH,
                                         blank=True)

    role = models.CharField('Роль пользователя',
                            choices=USERS_ROLES,
                            max_length=MAX_LENGTH,
                            blank=False,
                            default='user')

    groups = models.ManyToManyField(
        Group,
        related_name='yamdb_user_groups')
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='yamdb_user_permissions')

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
