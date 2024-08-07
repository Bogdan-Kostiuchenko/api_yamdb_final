from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import (UsersViewSet, TokenView, SignUpView)

v1_router = routers.DefaultRouter()
v1_router.register('users', UsersViewSet, basename='users')
v1_router.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include([
        path('signup/', SignUpView.as_view(), name='sign_up'),
        path('token/', TokenView.as_view(), name='get_token'),
    ])),
    path('token/', TokenObtainPairView.as_view())
]