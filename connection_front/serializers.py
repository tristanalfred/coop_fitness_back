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


class UploadProfilImageSerializer(serializers.HyperlinkedModelSerializer):
    # def apercu_image(self):
    #     u = Utilisateur.objects.get(username='qqchose2')
    #     u.last_name = 'brin'
    #     u.image_profil = Utilisateur.objects.get(username='user3').image_profil
    #     u.save()
    #     return Utilisateur.objects.get(username='user3').image_profil
    #
    # apercu_image(object)

    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'image_profil']


class TestUtilisateurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'image_profil']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'first_name', 'last_name', 'email', 'image_profil']
        read_only_fields = ['image_profil']


class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['image_profil']
