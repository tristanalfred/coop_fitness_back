import connection_front.permissions as perm

from rest_framework import viewsets
from connection_front.serializers import UtilisateurSerializer, VilleSerializer, UtilisateurChangeSerializer, \
    UtilisateurInscriptionSerializer, UtilisateurUploadProfileSerializer, UtilisateurUploadSerializer, MinimumUtilisateurSerializer
from connection_front.models import Ville, Utilisateur
from rest_framework import permissions, mixins

from rest_framework import status
from rest_framework import parsers
from rest_framework import response
from rest_framework.decorators import action
from rest_framework import filters


# Customs ViewSets
class ReadUpdateSingleModelViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet ne permettant que de visualiser et modifier un élément du modèle
    """
    pass


class CreateOnlyModelViewSet(viewsets.ViewSetMixin, viewsets.generics.CreateAPIView):
    """
    ViewSet ne permettant que de créer une instance du modèle
    """
    pass


class PutOnlyModelViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet ne permettant que de modifier une instance du modèle
    """
    pass


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de visualiser les utilisateurs et de les modifier
    """
    queryset = Utilisateur.objects.all().order_by('-date_joined')
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']


class VilleViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de visualiser les villes et de les modifier
    """
    queryset = Ville.objects.all().order_by('-id')
    serializer_class = VilleSerializer
    permission_classes = [perm.IsAdminOrAuthentifiedReadOnly]


class UtilisateurCompteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet permettant aux utilisateurs de visualiser leurs informations personnelles
    """
    queryset = Utilisateur.objects.all().order_by('-date_joined')
    serializer_class = UtilisateurSerializer
    permission_classes = [perm.IsAdminOrSelf]


class UtilisateurChangeViewSet(ReadUpdateSingleModelViewSet):
    """
    Vue permettant à un Utilisateur d'accéder à ses informations personnelles et de les modifier
    """
    queryset = Utilisateur.objects.all().order_by('-date_joined')
    serializer_class = UtilisateurChangeSerializer
    permission_classes = [perm.IsAdminOrSelf]


class UtilisateurInscriptionViewSet(CreateOnlyModelViewSet):
    """
    Vue permettant de créer un Utilisateur (inscription)
    """
    queryset = Utilisateur.objects.none()
    serializer_class = UtilisateurInscriptionSerializer
    permission_classes = [permissions.AllowAny]


class RechercheUtilisateurViewSet(viewsets.generics.ListAPIView):
    """
    Vue permettant de rechercher des utilisateurs
    """
    serializer_class = MinimumUtilisateurSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        username = self.kwargs['username']
        return Utilisateur.objects.filter(username=username)


class UploadProfileViewSet(PutOnlyModelViewSet):
    """
    Vue permettant à un utilisateur de changer sa photo de profil
    """
    serializer_class = UtilisateurUploadSerializer
    queryset = Utilisateur.objects.all()
    permission_classes = [perm.IsAdminOrSelf]

    @action(
        detail=True,
        methods=['PUT'],
        serializer_class=UtilisateurUploadProfileSerializer,
        parser_classes=[parsers.MultiPartParser]
    )
    def image_profil(self, request, pk):
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save(image_profil=request.FILES.get('image_profil'))
            return response.Response(serializer.data)
        return response.Response(serializer.errors,
                                 status.HTTP_400_BAD_REQUEST)
