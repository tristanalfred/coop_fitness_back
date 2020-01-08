from django.contrib import admin
from .models import DemandeInscription, Groupe, Invitation, MessageGroupe, MessagePrive, Permission, Suivi, \
    Utilisateur, Ville

admin.site.register(DemandeInscription)
admin.site.register(Groupe)
admin.site.register(Invitation)
admin.site.register(MessageGroupe)
admin.site.register(MessagePrive)
admin.site.register(Permission)
admin.site.register(Suivi)
admin.site.register(Utilisateur)
admin.site.register(Ville)
