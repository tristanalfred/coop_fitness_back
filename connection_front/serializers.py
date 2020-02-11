from rest_framework import serializers
from connection_front.models import DemandeInscription, Groupe, Invitation, MembreGroupe, Utilisateur, Ville


class GroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe
        fields = '__all__'


class UtilisateurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'email']


class UtilisateurChangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'ville', 'adresse']


class VilleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ville
        fields = ['id', 'nom']


class UtilisateurInscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utilisateur
        # fields = '__all__'
        exclude = ('password',)


class UtilisateurUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'first_name', 'last_name', 'email', 'image_profil']
        read_only_fields = ['image_profil']


class UtilisateurUploadProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['image_profil']


class MinimumUtilisateurSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['username', 'image_profil']


class MembreGroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembreGroupe
        fields = '__all__'


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'


class InvitationGroupeSerializer(serializers.ModelSerializer):
    """
    Serialise une invitations, mais remplace l'id du groupe par son nom
    """
    groupe = serializers.StringRelatedField()

    class Meta:
        model = Invitation
        fields = '__all__'


class DemandeInscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeInscription
        fields = '__all__'


class DemandeInscriptionUtilisateurSerializer(serializers.ModelSerializer):
    """
    Serialise une demande d'inscription, mais remplace l'id de l'expéditeur par son nom
    """
    expediteur = serializers.StringRelatedField()

    class Meta:
        model = DemandeInscription
        fields = '__all__'
