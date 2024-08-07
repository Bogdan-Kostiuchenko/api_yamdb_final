from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrSuperCanDestroy(BasePermission):
    
    def has_permission(self, request, view):
        if request.method not in ['PATCH', 'DELETE']:
            return (request.user.is_authenticated
                    and (request.user.is_superuser
                         or request.user.role == 'admin'))
        return True

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == 'admin'))


class IsAdminOrReadOnly(BasePermission):
    """Работать с пользователями может только администратор."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'admin'))


class IsAdminOrModeratorOrReadOnly(BasePermission):
    """Комментарии и отзывы доступны всем пользователям для чтения.
        Редактировать и удалять могут только автор, админ или модератор."""
    def has_permission(self, request, view):
        return request.method != 'POST' or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (obj.author == request.user
                    or request.user.is_superuser
                    or request.user.role == 'admin'
                    or request.user.role == 'moderator')
        return request.method in SAFE_METHODS
