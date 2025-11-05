import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than the last day."""
        old_question = Question(pub_date=timezone.now() - datetime.timedelta(days=1, seconds=1))
        self.assertIs(old_question.was_published_recently(), False)

    
    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date within the last day."""
        recent_question = Question(pub_date=timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59))
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=date)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """If no questions exist, return an appropriate message"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_questions_list"], [])

    def test_past_question(self):
        """past question will be displayed"""
        question = create_question("past question", -1)
        res = self.client.get(reverse("polls:index"))
        self.assertEqual(res.status_code, 200)
        self.assertQuerySetEqual(res.context["latest_questions_list"], [question])

    def test_future_question(self):
        """future question will be displayed"""
        create_question("future question", 1)
        res = self.client.get(reverse("polls:index"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "No polls are available.")
        self.assertQuerySetEqual(res.context["latest_questions_list"], [])

    def test_past_question_and_future_question(self):
        """only past questions are displayed"""
        create_question("future question", 1)
        question = create_question("past question", -1)
        res = self.client.get(reverse("polls:index"))
        self.assertEqual(res.status_code, 200)
        self.assertQuerySetEqual(res.context["latest_questions_list"], [question])

    def test_two_past_questions(self):
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["latest_questions_list"],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """future question should return 404 not found"""
        question = create_question("future question", 1)
        url = reverse("polls:details", args=(question.id,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)
    
    def test_past_question(self):
        """past question should display question text"""
        question = create_question("past question", -1)
        url = reverse("polls:details", args=(question.id, ))
        res = self.client.get(url)
        self.assertContains(res, question.question_text)
    