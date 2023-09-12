from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUser(BasePermission):
    message = 'У вас недостаточно прав для выполнения данного действия'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
