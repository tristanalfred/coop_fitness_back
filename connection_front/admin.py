from django.contrib import admin
from .models import DemandeInscription, Groupe, Invitation, MessageGroupe, MessagePrive, Permission, Suivi, \
    Utilisateur, Ville
from django.utils.html import mark_safe


class UtilisateurAdmin(admin.ModelAdmin):
    """
    Changements de l'affichage de l'utilisateur pour une meilleur visibilité sur la page d'administration
    """
    list_display = ('id', 'username', 'first_name', 'date_joined', 'apercu_image')
    list_filter = ('ville',)
    ordering = ('id', )
    search_fields = ('nom', 'prenom')

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


admin.site.register(DemandeInscription)
admin.site.register(Groupe)
admin.site.register(Invitation)
admin.site.register(MessageGroupe)
admin.site.register(MessagePrive)
admin.site.register(Permission)
admin.site.register(Suivi)
admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Ville)
