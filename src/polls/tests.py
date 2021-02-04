import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Question


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
