from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import serializers

from reviews.constans import NAME_MAX_LENGTH, EMAIL_MAX_LENGTH
from reviews.models import Category, Genre, Title, Review, Comment
from reviews import validators

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title
        read_only_fields = fields


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False,
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
        allow_empty=False
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class BaseReviewCommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        abstract = True


class ReviewSerializer(BaseReviewCommentSerializer):

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        if request.method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(
            title__id=title_id, author=request.user
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв о данном произведении.'
            )
        return data


class CommentSerializer(BaseReviewCommentSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ValidationMixin:

    def validate_username(self, value):
        return validators.validate_username(value)

    def validate_email(self, value):
        return validators.validate_email(value)


class GetTokenSerializer(serializers.Serializer, ValidationMixin):
    username = serializers.CharField(max_length=100)
    confirmation_code = serializers.CharField(max_length=100)


class SignUpSerializer(serializers.Serializer, ValidationMixin):
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        try:
            get_object_or_404(User,
                              email=email,
                              username=username)
        except Http404:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            else:
                raise ValidationError(f'Email {email} уже есть')
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            else:
                raise ValidationError(f'Username {username} уже есть')
        return data


class YamdbUserSerializer(serializers.ModelSerializer, ValidationMixin):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')


class YamdbUserSerializerWithoutRole(YamdbUserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        ordering = ('username',)
        exclude = ('role',)
