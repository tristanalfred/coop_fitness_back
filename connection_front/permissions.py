from rest_framework import permissions


class IsAdminOrSelf(permissions.BasePermission):
    """
    N'autorise l"accès qu'aux administrateurs et à l'utilisateur lui-même.
    """
    def has_object_permission(self, request, view, obj):
        # Administrateur
        if request.user and request.user.is_staff:
            return True

        # Propriétaire
        elif request.user and obj.id == request.user.id:
            return True

        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.id == request.user.id


class IsAdminOrAuthentifiedReadOnly(permissions.BasePermission):
    """
    Permission destiné à tous les modèles, dès lors qu'un utilisateur ne peut que lire les infos
    """
    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS) and (request.user.is_authenticated or request.user.is_staff):
            return True

        else:
            if request.user.is_staff:
                return True
            return False



"""
has_permission method will be called on all (GET, POST, PUT, DELETE) HTTP request.
has_object_permission method will not be called on HTTP POST request, hence we need to restrict it 
from has_permission method.
"""
