from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.generics import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.permissions import IsAdminOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from reviews.models import Category, Genre, Title
# from api_yamdb.api_yamdb import settings
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, SignUpSerializer,
                             GetTokenSerializer, YamdbUserSerializer)
from api.permissions import IsAdminOrReadOnly
from users.models import YamdbUser


class Main(mixins.ListModelMixin, mixins.CreateModelMixin,
           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'slug'


class CategoryViewSet(Main):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(Main):
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
            user = YamdbUser.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email')
            )
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
    permission_classes = (IsAdminOrReadOnly,)

    filter_backends = (filters.SearchFilter,)
    pagination_class = PageNumberPagination

    @action(
        methods=['GET', 'PATCH'], detail=False, url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_update_me(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            if self.request.method == 'PATCH':
                serializer.validated_data.pop('role', None)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
