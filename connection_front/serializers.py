from rest_framework import serializers
from connection_front.models import Utilisateur, Ville


class UtilisateurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'email']


class UtilisateurChangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email']


class VilleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ville
        fields = ['id', 'nom']


class UtilisateurInscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class UtilisateurUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'first_name', 'last_name', 'email', 'image_profil']
        read_only_fields = ['image_profil']


class UtilisateurUploadProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['image_profil']
