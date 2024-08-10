from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import YamdbUser
from users.validators import (
    validate_username, validate_email, check_role_exists
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False,
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        if request.method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(
            title_id=title_id, author=request.user
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв о данном произведении.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = YamdbUser
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        model = YamdbUser
        fields = ('username', 'email', 'role')

    def validate(self, data):
        validate_username(data['username'])

        if 'email' in data:
            validate_email(data['email'])

        if 'role' in data:
            check_role_exists(data['role'])
        return data


class YamdbUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = YamdbUser
        fields = '__all__'

    def validate(self, data):
        if 'username' in data:
            validate_username(data['username'])
        if 'email' in data:
            validate_email(data['email'])
        if 'role' in data:
            check_role_exists(data['role'])
        return data


class YamdbUserSerializerWithoutRole(serializers.ModelSerializer):
    """Сериализатор пользователей."""
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = YamdbUser
        ordering = ['username']
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio')

    def validate(self, data):
        if 'username' in data:
            validate_username(data['username'])
        if 'email' in data:
            validate_email(data['email'])
        return data
