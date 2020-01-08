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
    date_inscription = models.DateField()
    adresse = models.CharField(max_length=200, null=True)
    ville = models.ForeignKey('Ville', on_delete=models.CASCADE, verbose_name="ville", related_name='user_set',
                              null=True)

    def __str__(self):
        return self.last_name


class Permission(django.contrib.auth.models.Permission):

    def __str__(self):
        return self.name


class Groupe(django.contrib.auth.models.Group):
    visible = models.BooleanField(default=False)
    limited = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Ville(models.Model):
    nom = models.CharField(max_length=40)

    def __str__(self):
        return self.nom


class MessageGroupe(models.Model):
    expediteur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="expéditeur", related_name='+')
    groupe = models.ForeignKey('Groupe', on_delete=models.CASCADE, verbose_name="groupe", related_name='+')
    texte = models.CharField(max_length=300)
    date_envoi = models.DateField()


class MessagePrive(models.Model):
    expediteur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="expéditeur", related_name='+')
    destinataire = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="destinataire",
                                     related_name='+')
    texte = models.CharField(max_length=300)
    date_envoi = models.DateField()


class Invitation(models.Model):
    groupe = models.ForeignKey('Groupe', on_delete=models.CASCADE, verbose_name="groupe", related_name='+')
    destinataire = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="destinataire",
                                     related_name='+')
    date_invitation = models.DateField()
    texte = models.CharField(max_length=100, null=True)


class DemandeInscription(models.Model):
    destinataire = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="destinataire",
                                     related_name='+')
    groupe = models.ForeignKey('Groupe', on_delete=models.CASCADE, verbose_name="groupe", related_name='+')
    date_invitation = models.DateField()
    texte = models.CharField(max_length=100, null=True)


class Suivi(models.Model):
    interesse = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="interesse", related_name='+')
    concerne = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, verbose_name="concernte", related_name='+')
