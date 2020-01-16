import connection_front.permissions as perm
import io

from rest_framework import viewsets
from connection_front.serializers import UtilisateurSerializer, VilleSerializer, UtilisateurChangeSerializer, \
    UtilisateurInscriptionSerializer, UploadProfilImageSerializer, TestUtilisateurSerializer, ProfilePicSerializer, ProfileSerializer
from connection_front.models import Ville, Utilisateur
from rest_framework import permissions, mixins
import rest_framework.viewsets

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import parsers
from rest_framework import response
from rest_framework.decorators import action


# Customs ViewSets
class ReadUpdateSingleModelViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet ne permettant que de visualiser et modifier le modèle
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
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Utilisateur.objects.all().order_by('-date_joined')
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAdminUser]


class VilleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cities to be viewed or edited.
    """
    queryset = Ville.objects.all().order_by('-id')
    serializer_class = VilleSerializer
    permission_classes = [perm.IsAdminOrAuthentifiedReadOnly]


class UtilisateurChangeViewSet(ReadUpdateSingleModelViewSet):
    """
    Vue perrmettant à un Utilisateur d'accéder à ses informations personnelles et de les modifier
    """
    queryset = Utilisateur.objects.all().order_by('-date_joined')
    serializer_class = UtilisateurChangeSerializer
    permission_classes = [perm.IsAdminOrSelf]


class UtilisateurInscriptionViewSet(CreateOnlyModelViewSet):
    """
    Vue perrmettant de créer un Utilisateur
    """
    queryset = Utilisateur.objects.none()
    serializer_class = UtilisateurInscriptionSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET', 'PUT', 'PATCH'])
def UploadProfilImageViewSet(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        utilisateur = Utilisateur.objects.get(pk=pk)
    except Utilisateur.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = TestUtilisateurSerializer(utilisateur, data=request.data)
        if serializer.is_valid():
            # print(serializer.data)
            # print(request.data)
            # print(request.data.dict()['image_profile'])
            # utilisateur.image_profil.url = request.data.dict()['image_profile']
            # # utilisateur.image_profil.url = Utilisateur.objects.first().image_profil.url
            # utilisateur.image_profil.width = 100
            # utilisateur.image_profil.height = 100
            # utilisateur.save()

            # utilisateur.image_profil = data.image_profil
            # utilisateur.save()

            print(request.data)
            print(request.FILES)
            validatedData = serializer.validated_data
            print(validatedData)
            print(request.FILES.get('image_profil.url'))

            request.FILES.appendlist('image_profil.height', 100)
            request.FILES.appendlist('image_profil.width', 100)
            print(request.FILES.get('image_profil.height'))

            # user_profile = Utilisateur.objects.get(id=pk)
            # user_profile.image_profil.url = request.FILES.get('image_profil.url')

            serializer.save(image_profil=request.FILES.get('image_profil.url'))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Return this if request method is not POST
    return Response({'key': 'value'}, status=status.HTTP_200_OK)


class ProfileViewSet(PutOnlyModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Utilisateur.objects.all()
    permission_classes = [perm.IsAdminOrSelf]

    @action(
        detail=True,
        methods=['PUT'],
        serializer_class=ProfilePicSerializer,
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
