from http.client import BAD_REQUEST, OK

from django.http import Http404
from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, permissions, viewsets, status, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.permissions import (
    IsAdminOrReadOnly, IsAdmin, IsAuthorOrAdminOrModerator
)
from api.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer, ReviewSerializer,
    CommentSerializer, SignUpSerializer, GetTokenSerializer,
    YamdbUserSerializer, YamdbUserSerializerWithoutRole,
    TitleCreateUpdateSerializer
)
from reviews.models import Category, Genre, Title, Review, YamdbUser
from reviews.constans import EMAIL_ADMIN, RESERVE_USERNAME


class CategoryGenreMixinViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreMixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by(*Title._meta.ordering)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleCreateUpdateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrAdminOrModerator)
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrAdminOrModerator)
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def singup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data['username']
    email = request.data['email']

    try:
        user = get_object_or_404(YamdbUser,
                                 email=email,
                                 username=username)
    except Http404:
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
        serializer.save()
        user = get_object_or_404(YamdbUser,
                                 username=username)

    confirmation_code = default_token_generator.make_token(user)
    send_mail('Код подтверждения регистрации',
              f'Ваш код подтвержения: {confirmation_code}',
              EMAIL_ADMIN,
              [user.email])
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def token_jwt(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(YamdbUser,
                             username=serializer.validated_data["username"])
    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=OK)
    return Response(serializer.errors, status=BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = YamdbUserSerializer
    queryset = YamdbUser.objects.all()
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'], url_path='me',
            url_name=RESERVE_USERNAME, permission_classes=(IsAuthenticated,))
    def get_update(self, request):
        serializer = YamdbUserSerializer(request.user,
                                         data=request.data,
                                         partial=True)
        if request.method == 'PATCH':
            serializer = YamdbUserSerializerWithoutRole(request.user,
                                                        data=request.data,
                                                        partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
