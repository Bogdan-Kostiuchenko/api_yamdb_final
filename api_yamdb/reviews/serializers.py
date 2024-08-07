from django.db.models import Avg
from rest_framework import serializers

from .models import User, Category, Genre, Title, Review, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'role')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre', 'rating')

    def get_rating(self, obj):
        average_rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        return round(average_rating) if average_rating is not None else None


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        fields = ('title', 'text', 'author', 'score', 'pub_date')

    def validate_unique_title_author(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            if Review.objects.filter(title=data.get('title'),
                                     author=request.user).exists():
                raise serializers.ValidationError(
                    'Оставить отзыв о произведении можно только 1 раз. '
                    'Вы уже оставляли отзыв о данном произведении.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = ('review', 'text', 'author', 'pub_date')
