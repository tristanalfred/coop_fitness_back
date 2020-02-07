import datetime
import django.contrib.auth.models

from django.utils import timezone
from django.db import models


# Classes de test à supprimer une fois l'intégration continue en place
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# Classes courantes
class Utilisateur(django.contrib.auth.models.User):
    adresse = models.CharField(max_length=200, blank=True, null=True)
    ville = models.ForeignKey('Ville', on_delete=models.CASCADE, verbose_name="ville", related_name='user_set',
                              blank=True, null=True)
    image_profil = models.ImageField(blank=True, null=True, upload_to='images/')
    groupes = models.ManyToManyField('Groupe', blank=True, verbose_name="groupes", related_name='+')
    # notif_app = models.BooleanField(default=False)
    # notif_mail = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'utilisateur'
        verbose_name_plural = 'utilisateurs'

    def __str__(self):
        return self.last_name


class Permission(django.contrib.auth.models.Permission):

    def __str__(self):
        return self.name


class RoleUtilisateur(django.contrib.auth.models.Group):

    def __str__(self):
        return self.name


class Groupe(models.Model):
    nom = models.CharField(max_length=40)
    visible = models.BooleanField(default=False)
    limited = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class MembreGroupe(models.Model):
    membre = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="membre", related_name='+')
    groupe = models.ForeignKey('Groupe', on_delete=models.CASCADE, verbose_name="groupe", related_name='+')
    createur = models.BooleanField(default=False)
    responsable = models.BooleanField(default=False)

    class Meta:
        unique_together = ('membre', 'groupe')

    def __str__(self):
        return self.membre.username
        # return self.membre.username + ' | ' + \
        #        ('createur' if self.createur else 'responsable' if self.responsable else 'membre')


class Ville(models.Model):
    nom = models.CharField(max_length=40)

    def __str__(self):
        return self.nom


class MessageGroupe(models.Model):
    """
    Message d'un utilisateur destiné à un groupe
    """
    expediteur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="expéditeur", related_name='+')
    groupe = models.ForeignKey('Groupe', on_delete=models.CASCADE, verbose_name="groupe", related_name='+')
    texte = models.CharField(max_length=300)
    date_envoi = models.DateField()

    class Meta:
        verbose_name = "message de groupe"
        verbose_name_plural = "messages de groupe"


class MessagePrive(models.Model):
    """
    Message d'un utilisateur destiné à un autre utilisateur
    """
    expediteur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="expéditeur", related_name='+')
    destinataire = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="destinataire",
                                     related_name='+')
    texte = models.CharField(max_length=300)
    date_envoi = models.DateField()

    class Meta:
        verbose_name = "message privé"
        verbose_name_plural = "messages privé"


class Invitation(models.Model):
    """
    Invitation à rejoindre un groupe
    """
    groupe = models.ForeignKey('Groupe', on_delete=models.CASCADE, verbose_name="groupe", related_name='+')
    destinataire = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="destinataire",
                                     related_name='+')
    date_invitation = models.DateTimeField(default=django.utils.timezone.now)
    texte = models.CharField(max_length=100, null=True)
    accepte = models.BooleanField(null=True)

    class Meta:
        unique_together = ('groupe', 'destinataire')
        ordering = ['-id']


class DemandeInscription(models.Model):
    """
    Demande à rejoindre un groupe
    """
    expediteur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="expediteur",
                                   related_name='+')
    groupe = models.ForeignKey('Groupe', on_delete=models.CASCADE, verbose_name="groupe", related_name='+')
    date_invitation = models.DateTimeField(default=django.utils.timezone.now)
    texte = models.CharField(max_length=100, null=True)
    accepte = models.BooleanField(null=True)

    class Meta:
        verbose_name = "demande d'inscription"
        verbose_name_plural = "demandes d'inscription"
        unique_together = ('expediteur', 'groupe')
        ordering = ['-id']


class Suivi(models.Model):
    """
    Permet de suivre un autre utilisateur
    """
    interesse = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="interesse", related_name='+')
    concerne = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="concernte", related_name='+')
