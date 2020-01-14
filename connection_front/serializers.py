import django.contrib.auth.models
from rest_framework import serializers
from connection_front.models import Utilisateur, Ville


class UtilisateurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'email']


class UtilisateurChangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = django.contrib.auth.models.User
        fields = ['username', 'first_name', 'last_name', 'email']


class VilleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ville
        fields = ['id', 'nom']
