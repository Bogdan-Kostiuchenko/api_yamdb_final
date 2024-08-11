from rest_framework import serializers

from reviews.constans import USERS_ROLES, NAME_MAX_LENGTH, EMAIL_MAX_LENGTH
from reviews.models import Category, Genre, Title, Review, Comment, YamdbUser
from reviews import validators


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
    username = serializers.CharField(max_length=100,
                                     required=True)
    confirmation_code = serializers.CharField(max_length=100,
                                              required=True)

    def validate_username(self, value):
        return validators.validate_username(value)


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=NAME_MAX_LENGTH, required=True)
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH, required=True)

    class Meta:
        model = YamdbUser
        fields = ('username', 'email')

    def validate_username(self, value):
        return validators.validate_username(value)


class YamdbUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = YamdbUser
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')

    def validate_username(self, value):
        return validators.validate_username(value)


class YamdbUserSerializerWithoutRole(YamdbUserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = YamdbUser
        ordering = ('username',)
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')
