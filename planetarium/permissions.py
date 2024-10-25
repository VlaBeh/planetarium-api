from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminALLORIsAuthenticatedOReadOnly(BasePermission):
    """Allow authenticated users to create only reservations or tickets,
    and allow admins to perform any action. Unauthenticated users cannot access any views."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST' and view.basename in ['reservation', 'ticket']:
            return True

        return bool(request.user and request.user.is_staff)
