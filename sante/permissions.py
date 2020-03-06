from rest_framework import permissions
from connection_front.models import Utilisateur

"""
has_permission method will be called on all (GET, POST, PUT, DELETE) HTTP request.
has_object_permission method will not be called on HTTP POST request, hence we need to restrict it
from has_permission method.
"""


class ProgrammeGeneralPermission(permissions.BasePermission):
    """
    Permission n'autorisant la création de programmes généraux qu'aux administrateurs et coach,
    et la visualisation aux utilisateurs connectés.
    """
    def has_permission(self, request, view):
        if request.method == 'GET' and request.user.is_authenticated:
            return True
        elif request.method in ('POST', 'PUT', 'DELETE') \
                and request.user.is_authenticated \
                and request.user.is_staff:
            return True
        elif request.method in ('POST', 'PUT', 'DELETE') and request.user.is_authenticated:
            utilisateur = Utilisateur.objects.get(username=request.user.username)
            if utilisateur.is_coach:
                return True
        return False
