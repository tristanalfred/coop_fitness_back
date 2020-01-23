from rest_framework import permissions
from .models import DemandeInscription, Groupe

"""
has_permission method will be called on all (GET, POST, PUT, DELETE) HTTP request.
has_object_permission method will not be called on HTTP POST request, hence we need to restrict it 
from has_permission method.
"""


class IsAdminOrSelf(permissions.BasePermission):
    """
    Permission n'autorisant l'accès qu'aux administrateurs et à l'utilisateur lui-même.
    """
    def has_object_permission(self, request, view, obj):
        # Administrateur
        if request.user and request.user.is_staff:
            return True

        # Propriétaire
        elif request.user and obj.id == request.user.id:
            return True

        return False


class SelfExpedieur(permissions.BasePermission):
    """
    Permission n'autorisant un utilisateur qu'à poster des informations en son nom
    (information présente dans le Body de la requête POST)
    """
    def has_permission(self, request, view):
        if (request.method == 'POST') and (request.data['expediteur'] == str(request.user.id)):
            return True
        return False


class IsGoupCreator(permissions.BasePermission):
    """
    Permission n'autorisant que le créateur du groupe passé en paramètre à accéder à une information
    """
    def has_permission(self, request, view):
        if request.method == 'GET' \
                and Groupe.objects.get(id=view.kwargs.get('groupe_id')).createur.id == request.user.id \
                and request.user.is_authenticated:
            return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission n'autorisant que le propriétaire d'une instance de modèle à la modifier
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class IsAdminOrAuthentifiedReadOnly(permissions.BasePermission):
    """
    Permission ne permettant à un utilisateur que de visualiser les instances d'un modèle
    """
    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS) and (request.user.is_authenticated or request.user.is_staff):
            return True

        else:
            if request.user.is_staff:
                return True
            return False


class IsAdminOrAuthentifiedPostOnly(permissions.BasePermission):
    """
    Permission n'autorisant qu'à un utilisateur authentifié d'effectuer une action POST
    """
    def has_permission(self, request, view):
        if (request.method == 'POST') and (request.user.is_authenticated or request.user.is_staff):
            return True
        return False
