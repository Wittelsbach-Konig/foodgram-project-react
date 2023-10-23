from rest_framework.permissions import (SAFE_METHODS,
                                        BasePermission,
                                        IsAuthenticated)


class IsAdminOrReadOnly(BasePermission):
    """
    Пользовательское разрешение, позволяющее только
    чтение (safe methods) для пользователей,
    администраторам же позволяется выполнять любые действия.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )


class IsAuthorOrAdminOrReadOnly(IsAuthenticated):
    """
    Пользовательское разрешение, позволяющее только
    чтение (safe methods) для пользователей,
    администраторам и авторам же позволяется выполнять любые действия.
    """

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.is_admin
            or request.method in SAFE_METHODS
        )
