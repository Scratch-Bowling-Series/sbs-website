from rest_framework import permissions


class IsPrivateAllowed(permissions.BasePermission):
    """
    Allow access to request owner
    """
    def has_permission(self, request, view):
        # return True if allowed else False
        # 'username' is the request url kwarg eg. bobby, jonhdoe
        print(view.kwargs.get('id', ''))
        return view.kwargs.get('id', '') == request.user.id