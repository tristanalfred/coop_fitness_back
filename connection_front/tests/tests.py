import django.db.utils
import tempfile
import glob, os

from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from connection_front.models import DemandeInscription, Groupe, Invitation, MembreGroupe, Utilisateur
from PIL import Image


class UtilisateurTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Utilisateur.objects.create(username='user1', first_name='user1', last_name='user1', email='user1@user1.fr')
        Utilisateur.objects.create(username='user2', first_name='user2', last_name='user2', email='user2@user2.fr')

    def test_champs_utilisateur(self):
        utilisateur = Utilisateur.objects.get(username='user1')

        self.assertEqual(utilisateur.__str__(), 'user1')

    def test_utilisateur_duplique(self):
        with self.assertRaises(django.db.utils.IntegrityError):
            Utilisateur.objects.create(username='user1', first_name='user1', last_name='user1', email='user1@user1.fr')

    def test_get_tous_utilisateurs(self):
        utilisateurs = Utilisateur.objects.all()
        self.assertEqual(utilisateurs.count(), 2)


class MembreGroupeTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Utilisateur.objects.create(username='user1', first_name='user1', last_name='user1', email='user1@user1.fr')
        Utilisateur.objects.create(username='user2', first_name='user2', last_name='user2', email='user2@user2.fr')
        Groupe.objects.create(nom='groupe1')
        MembreGroupe.objects.create(membre=Utilisateur.objects.get(username='user1'), groupe=Groupe.objects.first(),
                                    createur=True)

    def test_membregroupe_duplique(self):
        with self.assertRaises(django.db.utils.IntegrityError):
            MembreGroupe.objects.create(membre=Utilisateur.objects.get(username='user1'), groupe=Groupe.objects.first())


class BasicAPITests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Utilisateur.objects.create(username='user1', first_name='user1', last_name='user1', email='user1@user1.fr',
                                   adresse='qqpart')
        Utilisateur.objects.create(username='user2', first_name='user2', last_name='user2', email='user2@user2.fr')

        Utilisateur.objects.create(username='admin', first_name='admin', last_name='admin', email='user1@user1.fr',
                                   is_staff=True, is_superuser=True)
        utilisateur_admin = Utilisateur.objects.get(username='admin')
        utilisateur_admin.set_password('admin')
        utilisateur_admin.save()

        utilisateur1 = Utilisateur.objects.get(username='user1')
        utilisateur1.set_password('mdp')
        utilisateur1.save()

        utilisateur2 = Utilisateur.objects.get(username='user2')
        utilisateur2.set_password('mdp')
        utilisateur2.save()

        cls.client_admin = APIClient()
        cls.client_admin.login(username='admin', password='admin')

        cls.client1 = APIClient()
        cls.client1.login(username='user1', password='mdp')

        cls.client2 = APIClient()
        cls.client2.login(username='user2', password='mdp')

        Groupe.objects.create(nom='groupe1')
        MembreGroupe.objects.create(membre=utilisateur1, groupe=Groupe.objects.first(), createur=True, responsable=True)


class UtilisateurTests(BasicAPITests):
    @classmethod
    def tearDownClass(cls):
        # Suppression des fichiers temporels créée pendant les tests
        for filename in glob.glob("media/images/tmp*"):
            os.remove(filename)
        super().tearDownClass()

    def test_inscription_utilisateur(self):
        """
        Inscription d'un nouvel utilisateur
        """
        url = reverse('inscription-list')
        data = {
            'username': 'testuser',
            'first_name': 'testuser',
            'last_name': 'testuser',
            'usertest': 'testuser',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Utilisateur.objects.filter(username='testuser').count(), 1)

    def test_get_list_utilisateur(self):
        """
        Recherche de la liste des utilisateurs
        """
        url = reverse('utilisateurs-list')
        response = self.client_admin.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_get_utilisateur(self):
        """
        Recherche d'un utilisateur
        """
        url = reverse('utilisateurs-detail', kwargs={'pk': '1'})
        response = self.client_admin.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_get_utilisateur_ko(self):
        """
        Recherche d'un utilisateur dont l'id est inexistant
        """
        url = reverse('utilisateurs-detail', kwargs={'pk': '100'})
        response = self.client_admin.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_change_utilisateur(self):
        """
        Modification d'un compte utilisateur
        """
        ancienne_adresse = Utilisateur.objects.get(username='user1').adresse
        url = reverse('change-detail', kwargs={'pk': '1'})
        data = {'username': 'user1', 'adresse': 'ailleurs'}
        self.client1.put(url, data, format='json')
        nouvelle_adresse = Utilisateur.objects.get(username='user1').adresse

        self.assertEqual(ancienne_adresse, 'qqpart')
        self.assertEqual(nouvelle_adresse, 'ailleurs')

    def test_api_change_utilisateur_ko(self):
        """
        Modification d'un autre compte utilisateur
        """
        url = reverse('change-detail', kwargs={'pk': '1'})
        data = {'username': 'user1', 'adresse': 'autre'}
        response = self.client2.put(url, data, format='json')
        nouvelle_adresse = Utilisateur.objects.get(username='user1').adresse

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(nouvelle_adresse, 'autre')

    def test_api_compte_utilisateur(self):
        """
        Visualisation d'un compte utilisateur
        """
        url = reverse('compte-detail', kwargs={'pk': '2'})
        response = self.client2.get(url, format='json')

        self.assertEqual(response.status_code, 200)

    def test_api_compte_utilisateur_ko(self):
        """
        Visualisation d'un autre compte utilisateur
        """
        url = reverse('compte-detail', kwargs={'pk': '2'})
        response = self.client1.get(url, format='json')

        self.assertEqual(response.status_code, 403)

    def test_api_upload_image_profile(self):
        with self.assertRaises(ValueError):
            _ancienne_image = Utilisateur.objects.get(id=2).image_profil.url

        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=True)
        image.save(tmp_file)
        tmp_file.seek(0)

        url = reverse('utilisateur-image-profil', kwargs={'pk': '2'})
        data = {'image_profil': tmp_file}
        response = self.client2.put(url, data, format='multipart')
        nouvelle_image = Utilisateur.objects.get(id=2).image_profil.url
        # os.remove(tmp_file.name)
        os.unlink(tmp_file.name)
        user = Utilisateur.objects.get(id=2)
        user.image_profil = None
        user.save()

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(nouvelle_image)


    def test_api_utilisateur_invitations(self):
        Invitation.objects.create(groupe=Groupe.objects.first(), destinataire=Utilisateur.objects.get(id=2))

        response = self.client2.get('/utilisateur/2/invitation', format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.items())[0][1], 1)

    def test_api_utilisateur_accepte_invitation(self):
        Invitation.objects.create(groupe=Groupe.objects.first(), destinataire=Utilisateur.objects.get(id=2))

        response = self.client2.patch('/utilisateur/2/accepte-invitation/1', format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invitation.objects.get(id=1).accepte, True)
        self.assertEqual(Utilisateur.objects.get(id=2).groupes.filter(groupe_id=1).count(), 1)

    def test_api_utilisateur_refuse_invitation(self):
        Invitation.objects.create(groupe=Groupe.objects.first(), destinataire=Utilisateur.objects.get(id=2))

        response = self.client2.patch('/utilisateur/2/refuse-invitation/1', format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invitation.objects.get(id=1).accepte, False)


class GroupeTests(BasicAPITests):
    def test_api_invitation(self):
        url = reverse('invitation-list')
        data = {
            'groupe': '1',
            'destinataire': '2'
        }
        response = self.client1.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invitation.objects.filter(groupe__id=1).count(), 1)

    def test_api_invitation_doublon_ko(self):
        url = reverse('invitation-list')
        data = {
            'groupe': '1',
            'destinataire': '2'
        }
        self.client1.post(url, data, format='json')
        response = self.client1.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Invitation.objects.filter(groupe__id=1).count(), 1)

    def test_api_invitation_autre_utilisateur_ko(self):
        url = reverse('invitation-list')
        data = {
            'groupe': '1',
            'destinataire': '2'
        }
        response = self.client2.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Invitation.objects.filter(groupe__id=1).count(), 0)

    def test_api_demande_inscription(self):
        url = reverse('demandeinscription-list')
        data = {
            'expediteur': '2',
            'groupe': '1'
        }
        response = self.client2.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DemandeInscription.objects.filter(groupe__id=1).count(), 1)

    def test_api_demande_inscription_doublon_ko(self):
        url = reverse('demandeinscription-list')
        data = {
            'expediteur': '2',
            'groupe': '1'
        }
        self.client2.post(url, data, format='json')
        response = self.client2.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(DemandeInscription.objects.filter(groupe__id=1).count(), 1)

    def test_api_demande_inscription_autre_utilisateur_ko(self):
        url = reverse('demandeinscription-list')
        data = {
            'expediteur': '2',
            'groupe': '1'
        }
        response = self.client1.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(DemandeInscription.objects.filter(groupe__id=1).count(), 0)

    def test_api_groupe_get_demande_inscription(self):
        url = reverse('demandeinscription-list')
        data = {
            'expediteur': '2',
            'groupe': '1'
        }
        self.client2.post(url, data, format='json')
        response = self.client1.get('/groupe/1/demande-inscription', format='json', follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.items())[0][1], DemandeInscription.objects.filter(groupe__id=1).count())

    def test_api_groupe_accepte_demande(self):
        url = reverse('demandeinscription-list')
        data = {
            'expediteur': '2',
            'groupe': '1'
        }
        self.client2.post(url, data, format='json')

        ancien_etat_demande = DemandeInscription.objects.get(id=1).accepte

        response = self.client1.patch('/groupe/1/accepte-demande/1', format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ancien_etat_demande, None)
        self.assertEqual(DemandeInscription.objects.get(id=1).accepte, True)
        self.assertEqual(MembreGroupe.objects.filter(membre__id=2).filter(groupe__id=1).count(), 1)

    def test_api_groupe_refuse_demande(self):
        url = reverse('demandeinscription-list')
        data = {
            'expediteur': '2',
            'groupe': '1'
        }
        self.client2.post(url, data, format='json')

        ancien_etat_demande = DemandeInscription.objects.get(id=1).accepte

        response = self.client1.patch('/groupe/1/refuse-demande/1', format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ancien_etat_demande, None)
        self.assertEqual(DemandeInscription.objects.get(id=1).accepte, False)

    def test_api_groupe_rend_responsable(self):
        MembreGroupe.objects.create(membre=Utilisateur.objects.get(id=2), groupe=Groupe.objects.first())

        response = self.client1.patch('/groupe/1/rend-responsable/2', format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MembreGroupe.objects.filter(groupe__id=1).get(membre__id=2).responsable, True)

    def test_api_groupe_retire_responsable(self):
        MembreGroupe.objects.create(membre=Utilisateur.objects.get(id=2), groupe=Groupe.objects.first(),
                                    responsable=True)

        response = self.client1.patch('/groupe/1/retire-responsable/2', format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MembreGroupe.objects.filter(groupe__id=1).get(membre__id=2).responsable, False)
