from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Name(models.Model):
    name = models.TextField(max_length=256)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Main(Name):
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        abstract = True


class Category(Main):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(Main):

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(Name):
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'жанр и произведение'
        verbose_name_plural = 'Жанры и произведения'

    def __str__(self):
        return f'Жанр произведения {self.title} - {self.genre}.'
