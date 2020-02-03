from django.contrib import admin
from .models import DemandeInscription, Groupe, RoleUtilisateur, Invitation, MessageGroupe, MessagePrive, Permission, \
    Suivi, Utilisateur, Ville
from django.utils.html import mark_safe
from django.contrib.auth.admin import UserAdmin


class UtilisateurAdmin(UserAdmin):
    """
    Changements de l'affichage de l'utilisateur pour une meilleur visibilité sur la page d'administration
    """
    list_display = ('id', 'username', 'first_name', 'date_joined', 'apercu_image')
    list_filter = ('ville',)
    ordering = ('id', )
    search_fields = ('nom', 'prenom')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'apercu_image', 'image_profil')}),
        ('Informations sociales', {'fields': ('adresse', 'ville', 'groupes')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),  # Ajouter RoleUtilisateur
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    filter_horizontal = ('groupes',)

    readonly_fields = ["apercu_image"]

    def apercu_image(self, obj):
        """
        Affiche un aperçu de l'image de profil. Sinon, affiche un logo par défault.
        :return: string contenant le code html servant à afficher l'image. Son contenu est reconnu comme correct.
        """
        if obj.image_profil:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.image_profil.url,
                width=50,
                height=50 * (obj.image_profil.height / obj.image_profil.width)
            ))
        else:
            return mark_safe('<img src="/media/images/default_user_profil.png" width=50 height=50 />')


class GroupeAdmin(admin.ModelAdmin):
    """
    Changements de l'affichage d'un groupe pour une meilleur visibilité sur la page d'administration
    """
    list_display = ('nom', 'createur', 'total_membres', 'id')
    ordering = ('id',)
    search_fields = ('nom',)

    readonly_fields = ["total_membres"]

    filter_horizontal = ('membres',)

    def total_membres(self, obj):
        return obj.membres.count()


class DemandeInscriptionAdmin(admin.ModelAdmin):
    """
    Changements de l'affichage d'une demande d'inscription
    """
    list_display = ('expediteur', 'groupe', 'date_invitation', 'texte')
    ordering = ('id',)


class InvitationAdmin(admin.ModelAdmin):
    """
    Changements de l'affichage d'une invitation
    """
    list_display = ('groupe', 'destinataire', 'date_invitation', 'texte')
    ordering = ('id',)


admin.site.register(DemandeInscription, DemandeInscriptionAdmin)
admin.site.register(RoleUtilisateur)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(MessageGroupe)
admin.site.register(MessagePrive)
admin.site.register(Permission)
admin.site.register(Suivi)
admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Ville)
admin.site.register(Groupe, GroupeAdmin)
