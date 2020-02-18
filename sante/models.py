from django.db import models
from django.utils import timezone
from django.db import models
from connection_front.models import Utilisateur
from django.template.defaultfilters import truncatechars


class Exercice(models.Model):
    nom = models.CharField(max_length=40)
    conseils = models.CharField(max_length=200, null=True, blank=True)

    @property
    def short_description(self):
        return truncatechars(self.conseils, 35)

    def __str__(self):
        return self.nom


class Serie(models.Model):
    exercice = models.ForeignKey('Exercice', on_delete=models.CASCADE, verbose_name="exercice")
    repetition = models.IntegerField()

    def __str__(self):
        return self.exercice.nom + " X " + str(self.repetition)


class Seance(models.Model):
    serie = models.ManyToManyField('Serie', verbose_name="series")
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    num_jour = models.IntegerField(null=True, blank=True)

    def __str__(self):
        resume = ''
        for s in self.serie.all():
            resume += (str(s) + ' + ')
        return resume


class ProgrammeSportIndividuel(models.Model):
    utilisateur = models.ForeignKey('connection_front.Utilisateur', on_delete=models.CASCADE)
    seance = models.ManyToManyField('Seance', verbose_name="seances")


class Programme(models.Model):
    nom = models.CharField(max_length=40)
    seance = models.ManyToManyField('Seance', verbose_name="seances")
    description = models.CharField(max_length=500, null=True, blank=True)

    @property
    def short_description(self):
        return truncatechars(self.description, 35)
