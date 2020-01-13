from rest_framework import viewsets
from connection_front.serializers import UtilisateurSerializer, VilleSerializer
from django.contrib.auth.models import User
from connection_front.models import Ville
from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class VilleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cities to be viewed or edited.
    """
    queryset = Ville.objects.all().order_by('-id')
    serializer_class = VilleSerializer
