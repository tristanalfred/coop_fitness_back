"""coop_fitness_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from connection_front import views
from sante import views as views_s
from django.conf import settings, urls
from django.conf.urls.static import static


router = routers.DefaultRouter(trailing_slash=False)

# URLs générales
router.register(r'users', views.UserViewSet, basename='utilisateur')
router.register(r'villes', views.VilleViewSet)
router.register(r'change', views.UtilisateurChangeViewSet, basename='change')
router.register(r'inscription', views.UtilisateurInscriptionViewSet, basename='inscription')
router.register(r'compte', views.UtilisateurCompteViewSet, basename='compte')
router.register(r'upload', views.UploadProfileViewSet)
router.register(r'invitation', views.InvitationViewSet)
router.register(r'demande-inscription', views.DemandeInscriptionViewSet)
router.register('message-prive', views.MessagePriveViewSet, basename='msg-prive')
router.register('message-groupe', views.MessageGroupeViewSet, basename='msg-groupe')  # POST

# URL santé
router.register(r'programmes-generaux', views_s.ProgrammeViewSet, basename='programme-general')
router.register(r'exercices', views_s.ExerciceViewSet, basename='exercice')
router.register(r'series', views_s.SerieViewSet, basename='serie')
router.register(r'seances', views_s.SeanceViewSet, basename='seance')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    urls.url('^recherche_utilisateur/(?P<username>.+)$', views.RechercheUtilisateurViewSet.as_view()),
    urls.url('^groupe/(?P<groupe_id>.+)/demande-inscription$', views.ManageDemandeInscriptionViewSet.as_view()),
    urls.url('^utilisateur/(?P<utilisateur_id>.+)/invitation$', views.ManageInvitationViewSet.as_view()),
    urls.url('^groupe/(?P<groupe_id>.+)/accepte-demande/(?P<demande_id>.+)$', views.AccepteDemandeAPIView.as_view()),
    urls.url('^groupe/(?P<groupe_id>.+)/refuse-demande/(?P<demande_id>.+)$', views.RefuseDemandeAPIView.as_view()),
    urls.url('^utilisateur/(?P<utilisateur_id>.+)/accepte-invitation/(?P<invitation_id>.+)$',
             views.AccepteInvitationAPIView.as_view()),
    urls.url('^utilisateur/(?P<utilisateur_id>.+)/refuse-invitation/(?P<invitation_id>.+)$',
             views.RefuseInvitationAPIView.as_view()),
    urls.url('^groupe/(?P<groupe_id>.+)/rend-responsable/(?P<membre_id>.+)$', views.RendResponsableAPIView.as_view()),
    urls.url('^groupe/(?P<groupe_id>.+)/retire-responsable/(?P<membre_id>.+)$', views.RetireResponsableAPIView.as_view()),
    urls.url('^creation-groupe$', views.CreationGroupeAPIView.as_view()),
    urls.url('^message-prive/(?P<destinataire_id>.+)$', views.MessagePriveViewSet.as_view({'get': 'list'}), name='msg'),
    urls.url('^message-groupe/(?P<groupe_id>.+)$', views.MessageGroupeViewSet.as_view({'get': 'list'}), name='msg-g'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
