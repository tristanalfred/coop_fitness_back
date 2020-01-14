import connection_front.permissions as perm

from rest_framework import viewsets
from connection_front.serializers import UtilisateurSerializer, VilleSerializer, UtilisateurChangeSerializer
from django.contrib.auth.models import User
from connection_front.models import Ville
from rest_framework import permissions, mixins
import rest_framework.viewsets


# Customs ViewSets
class ReadUpdateSingleModelViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet ne permettant que de visualiser et modifier le modèle
    """
    pass


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAdminUser]


class VilleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cities to be viewed or edited.
    """
    queryset = Ville.objects.all().order_by('-id')
    serializer_class = VilleSerializer
    permission_classes = [perm.IsAdminOrAuthentifiedReadOnly]


class UserViewChange(ReadUpdateSingleModelViewSet):
    """
    Vue perrmettant à un Utilisateur d'accéder à ses informations personnelles et de les modifier
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UtilisateurChangeSerializer
    permission_classes = [perm.IsAdminOrSelf]
