from rest_framework.permissions import SAFE_METHODS, BasePermission

from reviews.constans import USER_ROLE_MODERATOR, USER_ROLE_ADMIN


class IsAdminOrSuper(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return (request.user.is_authenticated
                    and (request.user.is_superuser
                         or request.user.role == USER_ROLE_ADMIN))
        return True

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == USER_ROLE_ADMIN))


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == USER_ROLE_ADMIN
                    or request.user.is_superuser))


class IsAuthorOrAdminOrModerator(BasePermission):
    """
    Разрешает редактировать и удалять комментарии только авторам,
    администраторам, модераторам и суперпользователям.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (request.user == obj.author
                or request.user.is_superuser
                or request.user.role in (USER_ROLE_ADMIN, USER_ROLE_MODERATOR))
