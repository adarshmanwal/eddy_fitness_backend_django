from rest_framework.permissions import BasePermission


class IsAdminUserRole(BasePermission):

    def has_permission(self, request, view):

        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "ADMIN"
        )


class IsTrainerUserRole(BasePermission):

    def has_permission(self, request, view):

        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "TRAINER"
        )


class IsAdminOrAssignedCenter(BasePermission):

    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:

            return False

        if request.user.role == "ADMIN":

            return True

        return obj in request.user.centers.all()