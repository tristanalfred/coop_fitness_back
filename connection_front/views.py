import connection_front.permissions as perm
from rest_framework import viewsets
from connection_front.serializers import DemandeInscriptionSerializer, DemandeInscriptionUtilisateurSerializer, \
    InvitationSerializer, InvitationGroupeSerializer, UtilisateurSerializer, VilleSerializer, \
    UtilisateurChangeSerializer, UtilisateurInscriptionSerializer, UtilisateurUploadProfileSerializer, \
    UtilisateurUploadSerializer, MinimumUtilisateurSerializer, MembreGroupeSerializer, GroupeSerializer
from connection_front.models import DemandeInscription, Groupe, Invitation, MembreGroupe, Utilisateur, Ville
from rest_framework import permissions, mixins
from rest_framework import status
from rest_framework import parsers
from rest_framework import response
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.views import APIView


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


class CreateReadOnlyViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    ViewSet ne permettant que de visualiser et créer une instance du modèle
    """
    pass


class DeleteOnlyViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    ViewSet ne permettant que de supprimer une instance du modèle
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


class InvitationViewSet(CreateOnlyModelViewSet):
    """
    Vue permettant au créateur d'un groupe d'envoyer une invitation à un utilisateur
    """
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.all()
    permission_classes = [perm.IsGroupCreatorPost]


class DemandeInscriptionViewSet(CreateReadOnlyViewSet):
    """
    Vue permettant à un utilisateur d'envoyer une demande d'inscription à un groupe
    """
    serializer_class = DemandeInscriptionSerializer
    queryset = DemandeInscription.objects.all()
    permission_classes = [perm.SelfExpedieur]


class ManageDemandeInscriptionViewSet(viewsets.generics.ListAPIView):
    """
    Vue permettant au créateur d'un groupe de visualiser toutes les demandes
    """
    serializer_class = DemandeInscriptionUtilisateurSerializer
    queryset = DemandeInscription.objects.all()
    permission_classes = [perm.IsGoupCreator]

    def get_queryset(self):
        groupe_id = self.kwargs['groupe_id']
        return DemandeInscription.objects.filter(groupe_id=groupe_id)


class ManageInvitationViewSet(viewsets.generics.ListAPIView):
    """
    Vue permettant à un utilisateur de visualiser toutes les invitations
    """
    serializer_class = InvitationGroupeSerializer
    queryset = Invitation.objects.all()
    permission_classes = [perm.IsSelfUtilisateurInPath]

    def get_queryset(self):
        utilisateur_id = self.kwargs['utilisateur_id']
        return Invitation.objects.filter(destinataire_id=utilisateur_id)


class AccepteDemandeAPIView(APIView):
    """
    Vue permettant à un createur de groupe d'accepter une demande d'inscription
    """
    permission_classes = [perm.IsGroupCreatorPatch]

    def patch(self, *_args, **kwargs):
        existe = DemandeInscription.objects.filter(id=kwargs.get('demande_id')).filter(
            groupe__id=kwargs.get('groupe_id')).count()
        if existe != 0:
            demande = DemandeInscription.objects.get(id=kwargs.get('demande_id'))
            demande.accepte = True
            demande.save()
            data = {
                'membre': DemandeInscription.objects.get(id=kwargs.get('demande_id')).expediteur.id,
                'groupe': kwargs.get('groupe_id'),
                'createur': False,
                'responsable': False
            }
            serializer = MembreGroupeSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return response.Response(status.HTTP_202_ACCEPTED)
        return response.Response(status.HTTP_404_NOT_FOUND)


class RefuseDemandeAPIView(APIView):
    """
    Vue permettant à un createur de groupe de refuser une demande d'inscription
    """
    permission_classes = [perm.IsGroupCreatorPatch]

    def patch(self, *_args, **kwargs):
        existe = DemandeInscription.objects.filter(id=kwargs.get('demande_id')).filter(
            groupe__id=kwargs.get('groupe_id')).count()
        if existe != 0:
            demande = DemandeInscription.objects.get(id=kwargs.get('demande_id'))
            demande.accepte = False
            demande.save()
            return response.Response(status.HTTP_202_ACCEPTED)
        return response.Response(status.HTTP_404_NOT_FOUND)


class AccepteInvitationAPIView(APIView):
    """
    Vue permettant à un utilisateur d'accepter une invitation
    """
    permission_classes = [perm.IsDestinatairePatch]

    def patch(self, *_args, **kwargs):
        existe = Invitation.objects.filter(id=kwargs.get('invitation_id')).filter(
            destinataire__id=kwargs.get('utilisateur_id')).count()
        if existe != 0:
            demande = Invitation.objects.get(id=kwargs.get('invitation_id'))
            demande.accepte = True
            demande.save()

            data = {
                'membre': kwargs.get('utilisateur_id'),
                'groupe': Invitation.objects.get(id=kwargs.get('invitation_id')).groupe.id,
                'createur': False,
                'responsable': False
            }
            serializer = MembreGroupeSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return response.Response(status.HTTP_202_ACCEPTED)
        return response.Response(status.HTTP_404_NOT_FOUND)


class RefuseInvitationAPIView(APIView):
    """
    Vue permettant à un utilisateur de refuser une invitation
    """
    permission_classes = [perm.IsDestinatairePatch]

    def patch(self, *_args, **kwargs):
        existe = Invitation.objects.filter(id=kwargs.get('invitation_id')).filter(
            destinataire__id=kwargs.get('utilisateur_id')).count()
        if existe != 0:
            demande = Invitation.objects.get(id=kwargs.get('invitation_id'))
            demande.accepte = False
            demande.save()
            return response.Response(status.HTTP_202_ACCEPTED)
        return response.Response(status.HTTP_404_NOT_FOUND)


class RendResponsableAPIView(APIView):
    """
    Vue permettant à un createur de groupe de donner les privilèges de responsable à un membre du groupe
    """
    permission_classes = [perm.IsGroupCreatorPatch]

    def patch(self, *_args, **kwargs):
        existe = MembreGroupe.objects.filter(groupe__id=kwargs.get('groupe_id')).filter(
            membre__id=kwargs.get('membre_id')).count()
        if existe != 0:
            membregroupe = MembreGroupe.objects.filter(groupe__id=kwargs.get('groupe_id')).get(
                membre__id=kwargs.get('membre_id'))
            membregroupe.responsable = True
            membregroupe.save()
            return response.Response(status.HTTP_202_ACCEPTED)
        return response.Response(status.HTTP_404_NOT_FOUND)


class RetireResponsableAPIView(APIView):
    """
    Vue permettant à un createur de groupe de retirer les privilèges de responsable à un membre du groupe
    """
    permission_classes = [perm.IsGroupCreatorPatch]

    def patch(self, *_args, **kwargs):
        existe = MembreGroupe.objects.filter(groupe__id=kwargs.get('groupe_id')).filter(
            membre__id=kwargs.get('membre_id')).count()
        if existe != 0:
            membregroupe = MembreGroupe.objects.filter(groupe__id=kwargs.get('groupe_id')).get(
                membre__id=kwargs.get('membre_id'))
            membregroupe.responsable = False
            membregroupe.save()
            return response.Response(status.HTTP_202_ACCEPTED)
        return response.Response(status.HTTP_404_NOT_FOUND)
