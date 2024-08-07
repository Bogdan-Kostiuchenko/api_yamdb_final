from django.contrib.auth.models import AbstractUser, Permission, Group
from django.core.validators import MaxLengthValidator
from django.db import models

from users.constans import NAME_MAX_LENGTH, EMAIL_MAX_LENGTH


class YamdbUser(AbstractUser):

    USERS_ROLES = [('user', 'Пользователь'),
                   ('moderator', 'Модератор'),
                   ('admin', 'Администратор')]

    username = models.SlugField('username пользователя',
                                max_length=NAME_MAX_LENGTH,
                                blank=False,
                                unique=True)
    first_name = models.CharField('Имя пользователя',
                                  max_length=NAME_MAX_LENGTH,
                                  validators=(MaxLengthValidator,),
                                  blank=True,)
    last_name = models.CharField('Фамилия',
                                 max_length=NAME_MAX_LENGTH,
                                 validators=(MaxLengthValidator,),
                                 blank=True,)
    email = models.EmailField('Электронная почта',
                              unique=True,
                              max_length=EMAIL_MAX_LENGTH)
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField('Код рeгистрации',
                                         max_length=NAME_MAX_LENGTH,
                                         blank=True)

    role = models.CharField('Роль пользователя',
                            choices=USERS_ROLES,
                            max_length=NAME_MAX_LENGTH,
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
