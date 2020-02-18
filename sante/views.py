from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from sante.serializers import ExerciceSerializer, ProgrammeSerializer, ProgrammeSportIndividuelSerializer, \
    SeanceSerializer, SerieSerializer
from sante.models import Exercice, Programme, ProgrammeSportIndividuel, Seance, Serie

import sante.permissions as perm
import connection_front.permissions as perm_g


# Create your views here.
class ProgrammeViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de visualiser les programmes généraux et de les modifier
    """
    queryset = Programme.objects.all().order_by('-id')
    serializer_class = ProgrammeSerializer
    # permission_classes = [perm.ProgrammeGeneralPermission]
    permission_classes = [permissions.AllowAny]


class ExerciceViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de visualiser les exercices et de les modifier
    """
    queryset = Exercice.objects.all().order_by('-id')
    serializer_class = ExerciceSerializer
    permission_classes = [permissions.AllowAny]


class SerieViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de visualiser les villes et de les modifier
    """
    queryset = Serie.objects.all().order_by('-id')
    serializer_class = SerieSerializer
    permission_classes = [permissions.AllowAny]


class SeanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de visualiser les villes et de les modifier
    """
    queryset = Seance.objects.all().order_by('-id')
    serializer_class = SeanceSerializer
    permission_classes = [permissions.AllowAny]
