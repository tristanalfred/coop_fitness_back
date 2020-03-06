from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from connection_front.models import Groupe, MembreGroupe, Utilisateur
from sante.models import Seance, Exercice, Programme, Serie, SeanceFav


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

        Exercice.objects.create(nom='test')

        Serie.objects.create(repetition=20, exercice=Exercice.objects.first())


class ProgrammeTests(BasicAPITests):
    def test_api_post_serie(self):
        serie_data = {'repetition': 20, 'exercice': 1}

        url = reverse('serie-plus-list')
        response = self.client2.post(url, serie_data, format='json')

        self.assertNotEqual(Serie.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_post_seance(self):
        seance_data = {
            'num_jour': 1,
            'serie': [
                {
                    'repetition': 20,
                    'exercice': 1
                },
                {
                    'repetition': 20,
                    'exercice': 1
                },
                {
                    'repetition': 30,
                    'exercice': 1
                },
            ],
        }

        url = reverse('seance-plus-list')
        response = self.client2.post(url, seance_data, format='json')

        self.assertNotEqual(Seance.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_non_duplication_serie(self):
        seance_data = {
            'num_jour': 1,
            'serie': [
                {
                    'repetition': 20,
                    'exercice': 1
                },
                {
                    'repetition': 20,
                    'exercice': 1
                },
                {
                    'repetition': 30,
                    'exercice': 1
                },
            ],
        }

        url = reverse('seance-plus-list')
        self.client2.post(url, seance_data, format='json')

        self.assertEqual(Serie.objects.filter(repetition=20).filter(exercice=Exercice.objects.first()).count(), 1)

    def test_create_programme_general(self):
        programme_data = {
            'nom': 'programme_test',
            'description': 'description',
        }
        url = reverse('programme-general-list')
        response = self.client_admin.post(url, programme_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Programme.objects.count(), 1)

    def test_create_programme_general_simple_utilisateur_ko(self):
        programme_data = {
            'nom': 'programme_test',
            'description': 'description',
        }
        url = reverse('programme-general-list')
        response = self.client2.post(url, programme_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Programme.objects.count(), 0)

    def test_create_seance_programme(self):
        programme_data = {
            'nom': 'programme_test',
            'description': 'description',
        }

        seance_data = {
            'programme_id': 1,
            'num_jour': 1,
        }

        url = reverse('programme-general-list')
        self.client_admin.post(url, programme_data, format='json')

        url_seance = reverse('programme-general-seance-list')
        response = self.client_admin.post(url_seance, seance_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Programme.objects.first().seance.count(), 1)
        self.assertEqual(str(Programme.objects.first().seance.first()), 'seance vide')

    # def test_update_seace_programme(self):
    #     programme_data = {
    #         'nom': 'programme_test',
    #         'description': 'description',
    #     }
    #
    #     seance_data = {
    #         'programme_id': 1,
    #         'num_jour': 1,
    #     }
    #
    #     seance_data_update = {
    #         'programme_id': 1,
    #         'num_jour': 1,
    #         'serie': [
    #             {
    #                 'repetition': 20,
    #                 'exercice': 1
    #             },
    #             {
    #                 'repetition': 20,
    #                 'exercice': 1
    #             },
    #             {
    #                 'repetition': 30,
    #                 'exercice': 1
    #             },
    #         ],
    #     }
    #
    #     url = reverse('programme-general-list')
    #     self.client_admin.post(url, programme_data, format='json')
    #
    #     url_seance = reverse('programme-general-seance-list')
    #     self.client_admin.post(url_seance, seance_data, format='json')
    #
    #     url_seance = reverse('programme-general-seance-detail', kwargs={'pk': '1'})
    #     self.client_admin.put(url_seance, seance_data_update, format='json')
