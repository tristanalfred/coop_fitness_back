from django.contrib import admin
from .models import DemandeInscription, Groupe, Invitation, MessageGroupe, MessagePrive, Permission, Suivi, \
    Utilisateur, Ville
from django.utils.html import mark_safe


class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'date_joined', 'apercu_image')
    list_filter = ('ville',)
    ordering = ('id', )
    search_fields = ('nom', 'prenom')

    readonly_fields = ["apercu_image"]

    def apercu_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image_profil.url,
            width=100,
            height=100 * (obj.image_profil.height / obj.image_profil.width),
        ))


admin.site.register(DemandeInscription)
admin.site.register(Groupe)
admin.site.register(Invitation)
admin.site.register(MessageGroupe)
admin.site.register(MessagePrive)
admin.site.register(Permission)
admin.site.register(Suivi)
admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Ville)
