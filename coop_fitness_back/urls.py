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
from django.conf import settings, urls
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet, base_name='utilisateurs')
router.register(r'villes', views.VilleViewSet)
router.register(r'change', views.UtilisateurChangeViewSet, base_name='change')
router.register(r'inscription', views.UtilisateurInscriptionViewSet, base_name='inscription')
router.register(r'compte', views.UtilisateurCompteViewSet, base_name='compte')
router.register(r'upload', views.UploadProfileViewSet)
router.register(r'invitation', views.InvitationViewSet)
router.register(r'demande-inscription', views.DemandeInscriptionViewSet)

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
    urls.url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    urls.url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    urls.url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
