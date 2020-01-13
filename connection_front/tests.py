import datetime
import django.db.utils

from django.test import TestCase
from django.utils import timezone

from .models import Question, Utilisateur


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
        self.assertEqual(0, 1)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


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
