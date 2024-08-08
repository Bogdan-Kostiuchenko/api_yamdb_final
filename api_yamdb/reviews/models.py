from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import YamdbUser


class NameSlugMixin(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(NameSlugMixin):

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(NameSlugMixin):

    class Meta:
        ordering = ('name',)
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'жанр и произведение'
        verbose_name_plural = 'Жанры и произведения'

    def __str__(self):
        return f'Жанр произведения {self.title} - {self.genre}.'


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(YamdbUser, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                                    MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    author = models.ForeignKey(YamdbUser, on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:20]
