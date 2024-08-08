from datetime import datetime as dt

from rest_framework import serializers

import users.validators as uservalid
from users.constans import USERS_ROLES
from users.models import YamdbUser
from reviews.models import Category, Genre, Title
from django.db.models import Avg

TITLES_MIN_YEAR = 1000


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        score = obj.reviews.aggregate(Avg('score'))
        return score['score__avg']


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
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        score = obj.reviews.aggregate(Avg('score'))
        return score['score__avg']

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
        uservalid.validate_username(data['username'])

        if 'email' in data:
            uservalid.validate_email(data['email'])

        if 'role' in data:
            uservalid.check_role_exists(data['role'])
        return data


class YamdbUserSerializer(serializers.ModelSerializer):
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
                  'bio',
                  'role')

    def validate(self, data):
        if 'username' in data:
            uservalid.validate_username(data['username'])
        if 'email' in data:
            uservalid.validate_email(data['email'])
        if 'role' in data:
            uservalid.check_role_exists(data['role'])
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
            uservalid.validate_username(data['username'])
        if 'email' in data:
            uservalid.validate_email(data['email'])
        return data
