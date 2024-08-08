from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrSuperCanDestroy(BasePermission):

    def has_permission(self, request, view):
        if request.method not in ['PATCH', 'DELETE', 'POST']:
            return (request.user.is_authenticated
                    and (request.user.is_superuser
                         or request.user.role == 'admin'))
        return True

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == 'admin'))


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'admin'
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
                or request.user.role in ('admin', 'moderator'))
