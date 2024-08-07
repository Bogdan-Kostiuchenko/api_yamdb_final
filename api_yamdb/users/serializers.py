from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import YamdbUser


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
        if value == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать username - me!'
            )
        return value


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

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Запрещено использовать username - me!'
            )
        return value

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
