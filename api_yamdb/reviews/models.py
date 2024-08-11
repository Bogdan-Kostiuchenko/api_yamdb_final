from django.core.validators import (MinValueValidator, MaxValueValidator)
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from reviews.constans import (MIN_SCORE, MAX_SCORE,
                              MIN_YEAR_PUB, NAME_MAX_LENGTH,
                              EMAIL_MAX_LENGTH, USERS_ROLES)


max_length = max([len(role) for role, _ in USERS_ROLES])


class YamdbUser(AbstractUser):

    username = models.SlugField('Никнейм пользователя',
                                max_length=NAME_MAX_LENGTH,
                                unique=True)
    first_name = models.CharField('Имя пользователя',
                                  max_length=NAME_MAX_LENGTH,
                                  blank=True,)
    last_name = models.CharField('Фамилия',
                                 max_length=NAME_MAX_LENGTH,
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
                            max_length=max_length,
                            blank=False,
                            default=USERS_ROLES[0][0])

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:50]


class NameSlug(models.Model):
    name = models.CharField(max_length=256, verbose_name='имя')
    slug = models.SlugField(
        max_length=50, verbose_name='уникальный идентификатор', unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)
        verbose_name = 'имя и уникальный идентификатор'
        verbose_name_plural = 'Имена и уникальные идентификаторы'

    def __str__(self):
        return self.name


class Category(NameSlug):

    class Meta(NameSlug.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlug):

    class Meta(NameSlug.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(
        validators=[
            MinValueValidator(MIN_YEAR_PUB),
            MaxValueValidator(timezone.now().year)
        ],
        verbose_name='год выпуска'
    )
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.text[:20]


class TextAuthorPubDate(models.Model):
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        YamdbUser, on_delete=models.CASCADE, related_name='%(class)ss',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='время публикации', auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:20]


class Review(TextAuthorPubDate):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='произведение'
    )
    score = models.PositiveIntegerField(
        verbose_name='оценка произведения',
        validators=[MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)]
    )

    class Meta(TextAuthorPubDate.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            ),
        )


class Comment(TextAuthorPubDate):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='отзыв'
    )

    class Meta(TextAuthorPubDate.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
