import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objectjs.create(question_text=question_text, pub_date=time)


class TestQuestionModel(TestCase):
    def test_was_published_recently_with_future_question(self):
        """It should return False if a question was published in the future."""
        future_date = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=future_date)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """It should return False if a question was published more than 1 day ago."""

        old_date = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=old_date)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """It should return True if a question was published until 1 day ago."""

        recent_date = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=recent_date)

        self.assertIs(recent_question.was_published_recently(), True)


class TestIndexView(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There aren't questions yet.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
