from rest_framework.permissions import (SAFE_METHODS,
                                        BasePermission,
                                        IsAuthenticatedOrReadOnly)


class IsAdminOrReadOnly(BasePermission):
    """
    Пользовательское разрешение, позволяющее только
    чтение (safe methods) для неавторизованных пользователей,
    администраторам же позволяется выполнять любые действия.

    """

    def has_permission(self, request, view):
        """
        Определяет, имеет ли пользователь разрешение
        на выполнение операции.

        Args:
            request (HttpRequest): Запрос, который проверяется
                на разрешение.
            view (View): Представление, к которому
                применяется разрешение.

        Returns:
            bool: True, если пользователь имеет разрешение,
                иначе False.
        """
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsAuthorOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Пользовательское разрешение, позволяющее только
    чтение (safe methods) для пользователей,
    администраторам и авторам же позволяется выполнять любые действия.
    """

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.is_superuser
            or request.method in SAFE_METHODS
        )
