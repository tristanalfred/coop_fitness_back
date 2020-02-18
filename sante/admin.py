from django.contrib import admin
from .models import Exercice, Programme, ProgrammeSportIndividuel, Serie, Seance
from django.contrib.auth.admin import UserAdmin


class ExerciceAdmin(admin.ModelAdmin):
    """
    Changement de l'affichage d'un utilisateur sur la page d'administration
    """
    list_display = ('id', 'nom', 'short_description')


class SeanceAdmin(admin.ModelAdmin):
    """
    Changement de l'affichage d'une séance sur la page d'administration
    """
    list_display = ('id',)
    filter_horizontal = ('serie',)


class ProgrammeAdmin(admin.ModelAdmin):
    """
    Changement de l'affichage d'une programme général sur la page d'administration
    """
    list_display = ('id', 'nom', 'short_description')
    filter_horizontal = ('seance',)


class ProgrammeSportIndividuelAdmin(admin.ModelAdmin):
    """
    Changement de l'affichage du programme d'un utilisateur sur la page d'administration
    """
    list_display = ('utilisateur',)


# Register your models here.
admin.site.register(Exercice, ExerciceAdmin)
admin.site.register(Serie)
admin.site.register(Seance, SeanceAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(ProgrammeSportIndividuel, ProgrammeSportIndividuelAdmin)
