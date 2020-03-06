from rest_framework import permissions
from .models import MembreGroupe

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


class IsSelfUtilisateurInPath(permissions.BasePermission):
    """
    Permission n'autorisant que l'utilisateur passé en paramètre à accéder à une information
    """
    def has_permission(self, request, view):
        if request.method == 'GET' \
                and view.kwargs.get('utilisateur_id') == str(request.user.id) \
                and request.user.is_authenticated:
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


class IsGroupCreatorPost(permissions.BasePermission):
    """
    Permission n'autorisant que le créateur du groupe passé en paramètre à créer un objet
    """
    def has_permission(self, request, view):
        is_creator = MembreGroupe.objects.filter(groupe__id=request.data['groupe']).filter(
            membre__id=request.user.id).filter(createur=True).count()
        if request.method == 'POST' and is_creator:
            return True
        return False


class IsGroupCreatorPatch(permissions.BasePermission):
    """
    Permission n'autorisant que le créateur du groupe passé en paramètre à modifier un objet
    """
    def has_permission(self, request, view):
        if request.method == 'PATCH' \
                and MembreGroupe.objects.filter(groupe__id=view.kwargs.get('groupe_id')).filter(membre__id=request.user.id).filter(createur=True).count() == 1 \
                and request.user.is_authenticated:
            return True
        return False


class IsDestinatairePatch(permissions.BasePermission):
    """
    Permission n'autorisant que le destinataire passé en paramètre à modifier un objet
    """
    def has_permission(self, request, view):
        if request.method == 'PATCH' \
                and view.kwargs.get('utilisateur_id') == str(request.user.id) \
                and request.user.is_authenticated:
            return True
        return False


class IsGoupCreator(permissions.BasePermission):
    """
    Permission n'autorisant que le créateur du groupe passé en paramètre à accéder à une information
    """
    def has_permission(self, request, view):
        if request.method == 'GET' \
                and MembreGroupe.objects.filter(groupe__id=view.kwargs.get('groupe_id')).get(createur=True).membre.id == request.user.id \
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


class MessagePrivePermission(permissions.BasePermission):
    """
    Permission autorisant l'envoie d'un message d'un utilisateur à un autre,
    ou d'accéder aux messages dont il est l'expéditeur ou le destinataire.
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST' and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' and obj.count() == 0 and request.user.is_authenticated:
            return True
        elif request.method == 'GET' \
                and (obj.first().expediteur.id == request.user.id or
                     view.kwargs.get('destinataire_id') == request.user.id) \
                and request.user.is_authenticated:
            return True
        return False


class MessageGroupePermission(permissions.BasePermission):
    """
    Permission autorisant l'envoie d'un message d'un utilisateur à un groupe auquel il appartient,
    ou d'accéder aux messages du groupe.
    """
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST' \
                and request.user.is_authenticated \
                and MembreGroupe.objects.filter(groupe__id=request.data.get('groupe')) \
                .filter(membre__id=request.user.id).count() == 1:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' \
                and request.user.is_authenticated \
                and MembreGroupe.objects.filter(groupe__id=view.kwargs.get('groupe_id'))\
                .filter(membre__id=request.user.id).count() == 1:
            return True

        return False
