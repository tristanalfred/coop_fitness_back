from django.db import models
from connection_front import models as m


class Exercice(models.Model):
    nom = models.CharField(max_length=40)

    def __str__(self):
        return self.nom


class Serie(models.Model):
    exercice = models.ForeignKey('Exercice', on_delete=models.CASCADE, verbose_name="exercice")
    repetition = models.IntegerField()

    def __str__(self):
        return self.exercice.nom + " X " + str(self.repetition)


class Seance(models.Model):
    serie = models.ManyToManyField('Serie', related_name='series', verbose_name="series")
