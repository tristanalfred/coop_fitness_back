from django.contrib import admin
from .models import DemandeInscription, Groupe, RoleUtilisateur, Invitation, MembreGroupe, MessageGroupe, MessagePrive, \
    Permission, Suivi, Utilisateur, Ville
from django.utils.html import mark_safe
from django.contrib.auth.admin import UserAdmin


class MembresGroupeAdmin(admin.TabularInline):
    model = MembreGroupe

    fieldsets = (
        (None, {'fields': ('groupe', 'createur', 'responsable')}),
    )

    readonly_fields = ["createur"]


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
        ('Informations sociales', {'fields': ('adresse', 'ville')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),  # Ajouter RoleUtilisateur
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    inlines = [MembresGroupeAdmin, ]

    readonly_fields = ['apercu_image']

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


class MembresAdmin(admin.TabularInline):
    model = MembreGroupe

    fieldsets = (
        (None, {'fields': ('membre', 'createur', 'responsable')}),
    )

    def get_readonly_fields(self, request, obj=None):
        if MembreGroupe.objects.filter(groupe__id=obj.id).filter(createur=True).count() != 0:
            return ['createur']
        return self.readonly_fields


class GroupeAdmin(admin.ModelAdmin):
    """
    Changements de l'affichage d'un groupe pour une meilleur visibilité sur la page d'administration
    """
    list_display = ('nom', 'createur', 'total_membres', 'id')
    ordering = ('id',)
    search_fields = ('nom',)

    fieldsets = (
        (None, {'fields': ('nom', 'createur', 'visible', 'limited', 'total_membres')}),
    )

    readonly_fields = ['total_membres', 'createur']

    # filter_horizontal = ('membres',)
    inlines = [MembresAdmin, ]

    def total_membres(self, obj):
        return MembreGroupe.objects.filter(groupe__id=obj.id).count()

    def createur(self, obj):
        return MembreGroupe.objects.filter(groupe__id=obj.id).get(createur=True)


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
admin.site.register(MembreGroupe)
