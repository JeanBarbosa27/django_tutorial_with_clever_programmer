import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionQuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """It should return False if a question was published in the future."""

        future_date = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=future_date)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        It should return False if a question was published more than 1 day ago.
        """

        old_date = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=old_date)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        It should return True if a question was published until 1 day ago.
        """

        recent_date = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=recent_date)

        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        It should be able to access the index page, but see that there's no
        question to be displayed and the context it's empty.
        """

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There aren't questions yet.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        It should displays questions the was created in the past,
        considering the actual date.
        """

        create_question(question_text='Past Question', days=-30)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past Question>']
        )

    def test_two_past_questions(self):
        """
        It should render at leat the last five past questions created.
        """

        create_question(question_text='Past Question 1', days=-30)
        create_question(question_text='Past Question 2', days=-1)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past Question 2>', '<Question: Past Question 1>']
        )



    def test_future_question(self):
        """
        It should not display any question in latest question list.
        """

        create_question(question_text='Future Question', days=30)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )

    def test_past_and_future_questions(self):
        """
        It should render only the past questions.
        """

        create_question(question_text='Past Question', days=-30)
        create_question(question_text='Future Question', days=30)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past Question>']
        )

class QuestionDetailViewTests(TestCase):
    def test_past_question(self):
        """
        It should render past questions detail page.
        """

        past_question = create_question(question_text='Past Question', days=-30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        """
        It should not render future questions detail page.
        """

        future_question = create_question(question_text='Future Question', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
