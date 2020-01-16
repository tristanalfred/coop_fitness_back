import django.db.utils

from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase
# from rest_framework.test import APIRequestFactory
from connection_front.models import Utilisateur


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


class UtilisateurTests(APITestCase):
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
        self.assertEqual(Utilisateur.objects.count(), 1)
        self.assertEqual(Utilisateur.objects.get().username, 'testuser')
