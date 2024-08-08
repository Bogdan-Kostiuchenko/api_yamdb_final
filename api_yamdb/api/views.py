from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


from api.permissions import IsAdminOrReadOnly, IsAdminOrSuperCanDestroy
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, SignUpSerializer,
                             GetTokenSerializer, YamdbUserSerializer,
                             YamdbUserSerializerWithoutRole)
from reviews.models import Category, Genre, Title
from users.models import YamdbUser


def check_users(username, email):
    try:
        YamdbUser.objects.get(email=email)
    except YamdbUser.DoesNotExist:
        pass
    else:
        return Response({'detail': f'Email {email} уже есть'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        YamdbUser.objects.get(username=username)
    except YamdbUser.DoesNotExist:
        pass
    else:
        return Response({'detail': 'Username {username} уже есть'},
                        status=status.HTTP_400_BAD_REQUEST)

    return None


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class SignUpView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get('email')
            username = request.data.get('username')

            if YamdbUser.objects.filter(email=email,
                                        username=username).exists():
                return Response({'detail': 'Пользователь уже зарегистрирован'},
                                status=status.HTTP_200_OK)

            checking = check_users(username, email)
            if checking is not None:
                return checking

            serializer.save()
            user = YamdbUser.objects.get(
                username=username,
                email=email
                )
            confirmation_code = default_token_generator.make_token(user)
            send_mail('Код подтверждения регистрации',
                      f'Ваш код подтвержения: {confirmation_code}',
                      'admin@mail.ru',
                      [email])
            return Response(request.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                YamdbUser, username=request.data.get('username')
            )
            if not default_token_generator.check_token(
                user, request.data.get('confirmation_code')
            ):
                return Response('Неверный код',
                                status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            token = {'token': str(refresh.access_token)}
            return Response(token, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = YamdbUserSerializer
    queryset = YamdbUser.objects.order_by('pk')
    permission_classes = (IsAdminOrReadOnly,
                          IsAdminOrSuperCanDestroy)

    filter_backends = (filters.SearchFilter,)
    pagination_class = PageNumberPagination

    lookup_field = 'username'
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'], url_path='me',
            url_name='me', permission_classes=(IsAuthenticated,))
    def get_update_me(self, request):
        serializer = YamdbUserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = None
            if 'role' in request.data:
                serializer = YamdbUserSerializerWithoutRole(
                        request.user, data=request.data, partial=True
                    )
            else:
                serializer = YamdbUserSerializer(
                    request.user, data=request.data, partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        checking = check_users(username, email)
        if checking is not None:
            return checking

        serializer = YamdbUserSerializerWithoutRole(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
