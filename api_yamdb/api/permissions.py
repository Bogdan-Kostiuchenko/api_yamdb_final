from rest_framework.permissions import SAFE_METHODS, BasePermission

from reviews.constans import MODERATOR, ADMIN


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == ADMIN))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == ADMIN))


class IsAdminOrReadOnly(IsAdmin):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == ADMIN
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
                or request.user.is_staff
                or request.user.role in (ADMIN, MODERATOR))
