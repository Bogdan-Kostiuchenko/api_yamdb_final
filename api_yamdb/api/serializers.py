import users.validators as uservalid
from rest_framework import serializers

from users.models import YamdbUser
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = YamdbUser
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):
    # username = serializers.CharField()
    # email = serializers.EmailField()

    class Meta:
        model = YamdbUser
        fields = ('username', 'email')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=YamdbUser.objects.all(),
                fields=('username', 'email'),
                message=' Пользователь с таким именем уже существует!'
            )
        ]

    def validate_username(self, value):
        return uservalid.validate_username(value)


class YamdbUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = YamdbUser
        ordering = ['username']
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')

    # def validate_username(self, value):
    #     if value == 'me':
    #         raise serializers.ValidationError(
    #             'Запрещено использовать username - me!'
    #         )
    #     return value

    def validate_username(self, username):
        """Проверка логина."""
        return uservalid.validate_username(username)

    def validate_email(self, email):
        """Проверка email."""
        return uservalid.validate_email(email)

# class AdminUserSerializer(serializers.ModelSerializer):
#     """Сериалайзер для пользователя с ролью 'admin'."""

#     class Meta:
#         model = YamdbUser
#         ordering = ('username')
#         fields = ('username',
#                   'email',
#                   'bio',
#                   'role',)

#     def validate_username(self, value):
#         if self.initial_data.get('username') == 'me':
#             raise serializers.ValidationError(
#                 'Запрещено использовать username - me!'
#             )
#         return value
