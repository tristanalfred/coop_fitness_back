import django.db.utils

from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from connection_front.models import Groupe, MembreGroupe, Utilisateur
from requests.auth import HTTPBasicAuth


class UtilisateurTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Utilisateur.objects.create(username='user1', first_name='user1', last_name='user1', email='user1@user1.fr')
        Utilisateur.objects.create(username='user2', first_name='user2', last_name='user2', email='user2@user2.fr')

        # client = APIClient()
        # client.login(username='admin', password='admin')

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


class UtilisateurTests(APITestCase):
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
        Modification d'un compte utilisateur
        """
        url = reverse('change-detail', kwargs={'pk': '1'})
        data = {'username': 'user1', 'adresse': 'autre'}
        response = self.client2.put(url, data, format='json')
        nouvelle_adresse = Utilisateur.objects.get(username='user1').adresse

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(nouvelle_adresse, 'autre')
