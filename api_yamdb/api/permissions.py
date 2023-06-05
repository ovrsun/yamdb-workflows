from rest_framework import permissions


class IsAuthorModeratorAdminOrReadOnlyPermission(permissions.BasePermission):
    """
    Обеспечивает доступ автору, модератору и админу.
    Все остальные - безопасные методы.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Обеспечивает доступ админу и user. Все остальные - безопасные методы."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """Обеспечивает доступ админу. Все остальные - безопасные методы."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin or request.user.is_superuser)
        return request.method in permissions.SAFE_METHODS


class AdminOnly(permissions.BasePermission):
    """Обеспечивает доступ только aдмину."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_staff
                or request.user.is_admin
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.is_staff
                or request.user.is_admin
            )
        return False
