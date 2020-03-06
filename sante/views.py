from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import response
from rest_framework import status
from sante.serializers import ExerciceSerializer,  SerieReadSerializer, \
    SeanceReadSerializer, SeanceTestSerializer, SerieSerializer, SeancePlusSerializer, SeriePlusSerializer, \
    SeanceFavSerializer, ProgrammeSerializer, SeanceProgrammeSerializer, SeanceCreateProgrammeSerializer
from sante.models import Exercice, Programme, Seance, SeanceFav, SeanceProgramme, Serie
from connection_front.models import Utilisateur

import sante.permissions as perm


# Create your views here.
class ExerciceViewSet(viewsets.ModelViewSet):  # TODO : on garde
    """
    ViewSet permettant de visualiser les exercices et de les modifier
    """
    queryset = Exercice.objects.all().order_by('-id')
    serializer_class = ExerciceSerializer
    permission_classes = [perm.ProgrammeGeneralPermission]


class SerieViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de visualiser les villes et de les modifier
    """
    queryset = Serie.objects.all().order_by('-id')
    # serializer_class = SerieSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return SerieReadSerializer
        return SerieSerializer


class SeanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de visualiser les villes et de les modifier
    """
    queryset = Seance.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return SeanceReadSerializer
        return SeanceTestSerializer

    # serializer_class = SeanceSerializer
    permission_classes = [permissions.AllowAny]


class SeriePlusViewSet(viewsets.ModelViewSet):  # TODO : on garde
    """
    ViewSet permettant de visualiser les programmes généraux et de les modifier
    """
    queryset = Serie.objects.all().order_by('-id')
    serializer_class = SeriePlusSerializer
    permission_classes = [permissions.AllowAny]


class SeancePlusViewSet(viewsets.ModelViewSet):  # TODO : on garde
    """
    ViewSet permettant de visualiser les programmes généraux et de les modifier
    """
    queryset = Seance.objects.all().order_by('-id')
    serializer_class = SeancePlusSerializer
    permission_classes = [permissions.AllowAny]


class SeanceFavViewSet(viewsets.ModelViewSet):
    queryset = SeanceFav.objects.all()
    serializer_class = SeanceFavSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = SeanceFav.objects\
            .filter(utilisateur=Utilisateur.objects.get(id=request.user.id))

        self.check_object_permissions(self.request, queryset)
        serializer = SeanceFavSerializer(queryset, context={'request': request}, many=True)
        return response.Response(serializer.data)


class ProgrammeViewSet(viewsets.ModelViewSet):  # TODO : on garde
    """
    ViewSet permettant de visualiser les programmes généraux et de les modifier
    """
    queryset = Programme.objects.all().order_by('-id')
    serializer_class = ProgrammeSerializer
    permission_classes = [perm.ProgrammeGeneralPermission]
    # permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        data = {
            'nom': list(request.data.items())[0][1],
            'description': list(request.data.items())[1][1],
            'createur': Utilisateur.objects.get(id=request.user.id)
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(status.HTTP_200_OK)
        return response.Response(serializer.errors,
                                 status.HTTP_400_BAD_REQUEST)


class SeanceProgrameViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de visualiser les programmes généraux et de les modifier
    """
    queryset = SeanceProgramme.objects.all()
    serializer_class = SeanceProgrammeSerializer
    # permission_classes = [perm.ProgrammeGeneralPermission]
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method not in ['POST']:
            print('pas post')
            return SeanceCreateProgrammeSerializer
        return SeanceProgrammeSerializer

    def create(self, request, *args, **kwargs):
        data = {
            'num_jour': request.data['num_jour']
        }
        serializer_seance = self.serializer_class(data=data)
        if serializer_seance.is_valid():
            serializer_seance.save()

            programme = Programme.objects.get(id=request.data['programme_id'])
            seance = SeanceProgramme.objects.get(id=serializer_seance.data['id'])

            # Ajout de la séance au programme
            programme.seance.add(seance)
            programme.save()

            return response.Response(status.HTTP_200_OK)
        return response.Response(serializer_seance.errors,
                                 status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     # print(request)
    #     # print(request.data)
    #     # print(args)
    #     # print(kwargs)
