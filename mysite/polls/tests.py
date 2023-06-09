import datetime
from django.urls import reverse

from django.test import TestCase
from django.utils import timezone

from .models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True) 

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    if days != None:
        time = timezone.now() + datetime.timedelta(days=days)
    else:
        time = None
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        '''Questions with a pub_date in the past are displayed on the index page'''
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question],)

    def test_future_question(self):
        '''Questions with pub_date in the future aren't displayed on the index page.'''
        create_question(question_text = "Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days =- 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text = "Past question 1.", days=-30)
        question2 = create_question(question_text = "Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question2, question1])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text = 'Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,)) #the comma is needed b/c *args are always tuples. tuples can't have one item
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class ChoiceModelTests(TestCase):

    def test_question_has_choices(self):
        '''The detail view of a question has choices available'''
        sample_question = create_question(question_text = 'Question has choices.', days = 0)
        sample_choice = sample_question.choice_set.create(choice_text = 'Some choice text.', votes = 0)
        url = reverse('polls:detail', args=(sample_question.id,))
        response = self.client.get(url)
        self.assertContains(response, sample_choice)
        self.assertTrue(sample_question.choice_set.count() > 0)
    
    def test_question_without_choices_is_unpublished(self):
        '''A question without any choices available will not be published '''
        sample_question = create_question(question_text = "Question without choices is unpublished", days = None)
        #no choices created
        self.assertTrue(sample_question.pub_date == None)



    

# todo: Write a test that checks that questions have choices available and that it is not published if it does not

#todo: Write test that checks that admin can unpublish questions, but standard users cannot