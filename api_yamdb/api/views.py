from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.generics import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.permissions import IsAdminOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django.core.exceptions import ValidationError 

from reviews.models import Category, Genre, Title
# from api_yamdb.api_yamdb import settings
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, SignUpSerializer,
                             GetTokenSerializer, YamdbUserSerializer)
from api.permissions import IsAdminOrReadOnly, IsAdminOrModeratorOrReadOnly, IsAdminOrSuperCanDestroy
from users.models import YamdbUser


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
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                YamdbUser, username=serializer.validated_data["username"]
                )
            # user = YamdbUser.objects.get(
            #     username=request.data.get('username'),
            #     email=request.data.get('email')
            # )
            confirmation_code = default_token_generator.make_token(user)
            send_mail('Код подтверждения регистрации',
                      f'Ваш код подтвержения: {confirmation_code}',
                      'admin@mail.ru',
                      [request.data.get('email')])
            return Response(serializer.data, status=status.HTTP_200_OK)
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
    lookup_value_regex = r'[\w\@\.\+\-]+'
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'], url_path='me',
            url_name='me', permission_classes=(IsAuthenticated,))
    def about_me(self, request):
        serializer = YamdbUserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = YamdbUserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(
    #     methods=['GET', 'PATCH'], detail=False, url_path='me',
    #     permission_classes=(IsAuthenticated,)
    # )
    # def get_update_me(self, request):
    #     serializer = self.get_serializer(
    #         request.user,
    #         data=request.data,
    #         partial=True
    #     if serializer.is_valid():
    #         if self.request.method == 'PATCH':
    #             serializer.validated_data.pop('role', None)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(
    #         serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #     )
    #     )

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


    # def destroy(self, request, username):
    #     if username == 'me':
    #         return Response(
    #             {'error': 'Нельзя удалить себя!'},
    #             status=status.HTTP_405_METHOD_NOT_ALLOWED
    #         )
    #     return super().destroy(request, username)