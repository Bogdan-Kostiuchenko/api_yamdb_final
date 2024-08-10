from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from reviews.constans import MIN_SCORE, MAX_SCORE, MIN_YEAR_PUB
from users.models import YamdbUser


class NameSlugMixin(models.Model):
    name = models.CharField(max_length=256, verbose_name='имя')
    slug = models.SlugField(max_length=50, verbose_name='слаг', unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)
        verbose_name = 'имя и слаг'
        verbose_name_plural = 'Имена и слаги'

    def __str__(self):
        return self.name


class Category(NameSlugMixin):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugMixin):

    class Meta:
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


class ReviewCommentModel(models.Model):
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
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:20]


class Review(ReviewCommentModel):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='произведение'
    )
    score = models.PositiveIntegerField(
        verbose_name='оценка произведения',
        validators=[MinValueValidator(MIN_SCORE), MaxValueValidator(MAX_SCORE)]
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            ),
        )


class Comment(ReviewCommentModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='отзыв'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
