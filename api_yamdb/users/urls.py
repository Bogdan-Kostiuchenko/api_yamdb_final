from django.urls import path, include
from rest_framework import routers

from users.views import (UsersViewSet, TokenView, SignUpView)

v1_router = routers.DefaultRouter()
v1_router.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/signup/', SignUpView.as_view(), name='sign_up'),
    path('auth/token/', TokenView.as_view(), name='get_token')
]
