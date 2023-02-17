from .api import *
from .model_factories import *
from .models import *
from .serializers import *
from .views import *
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.urls import reverse_lazy
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
import factory
import json
from http import HTTPStatus
from django.contrib.sessions.middleware import SessionMiddleware


class TestUserCanCreateImageAndViewListOfOwnImages(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        appuser = AppUserFactory.create()
        self.user = appuser.user
        # self.user = User.objects.create_user(
        #     username='jacobs', email='jacob@…', password='top_secret', appuser=AppUserFactory.create())

    def test_details(self):
        ImageFactory.create(user=self.user.appuser)

        # Create an instance of a GET request.
        request = self.factory.get('/api/images/')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Use this syntax for class-based views.
        response = ImageList.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestUserCanAddFriendsSuccessfully(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        appuser = AppUserFactory.create()
        friend1 = AppUserFactory.create()
        self.user = appuser.user
        self.friend1 = friend1
        self.good_url = reverse('final_main_app:add_friend', kwargs={
                                'friend_username': friend1.user.username})
        self.destination_url = '/my-friends/'

    def test_add_friends_endpoint_redirect_success(self):

        # Create an instance of a GET request.
        request = self.factory.get(self.good_url)

        # Add support django messaging framework
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        response = addFriend(request, self.friend1.user.username)

        response.client = Client()
        self.assertRedirects(response, self.destination_url,
                             target_status_code=302)

    def test_add_friends_endpoint_friends_added(self):
        # Initially user will have no friends
        self.assertEqual(self.user.appuser.friends.count(), 0)

        # Create an instance of a GET request.
        request = self.factory.get(self.good_url)

        # Add support django messaging framework
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Use this syntax for class-based views.
        response = addFriend(request, self.friend1.user.username)

        # user should have one friend now, re-fetch user from DB
        fresh_app_user = AppUser.objects.get(user=self.user)

        response.client = Client()
        self.assertRedirects(response, self.destination_url,
                             target_status_code=302)

        # check that user has one friend
        self.assertEqual(fresh_app_user.friends.count(), 1)


class TestUserCanCreateQuestion(TestCase):
    def setUp(self):
        appuser = AppUserFactory.create()
        self.category = CategoryFactory.create()
        self.user = appuser.user
        self.factory = RequestFactory()

    def test_add_question_endpoint_redirect_success(self):
        title = 'Test title test_add_question_endpoint_redirect_success'
        request = self.factory.post('/ask-question/', data={
            'category': self.category.id,
            'title': title,
            'content': '{"delta":"{\\"ops\\":[{\\"insert\\":\\"Lorem Ipsum\\"},{\\"attributes\\":{\\"align\\":\\"center\\",\\"header\\":1},\\"insert\\":\\"\\\\n\\"},{\\"attributes\\":{\\"italic\\":true},\\"insert\\":\\"\\\\\\"Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...\\\\\\"\\"},{\\"attributes\\":{\\"align\\":\\"center\\",\\"header\\":4},\\"insert\\":\\"\\\\n\\"},{\\"insert\\":\\"\\\\\\"There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...\\\\\\"\\"},{\\"attributes\\":{\\"align\\":\\"center\\",\\"header\\":5},\\"insert\\":\\"\\\\n\\"},{\\"insert\\":\\"\\\\n\\"}]}","html":"<h1 class=\\"ql-align-center\\">Lorem Ipsum</h1><h4 class=\\"ql-align-center\\"><em>\\"Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...\\"</em></h4><h5 class=\\"ql-align-center\\">\\"There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...\\"</h5><p><br></p>"}',
            'action': 'SAVE'
        })

        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        request.user = self.user
        response = AskQuestionView.as_view()(request)
        self.assertEqual(response.status_code, 302)

        question = Question.objects.all().first()

        self.assertEqual(question.title, title)
        self.assertEqual(question.user.id, self.user.id)


class TestUserCanCreateAnswer(TestCase):
    def setUp(self):
        # appuser = AppUserFactory.create()
        # self.user = appuser.user
        self.question = QuestionFactory.create()
        self.factory = RequestFactory()

    def test_add_answer_endpoint_redirect_success(self):
        Badge.objects.create(name='Hub badge')
        request = self.factory.post('/question/' + str(self.question.id) + '/answer/', data={
            'action': 'SAVE',
            'category': self.question.category.id,
            'question': self.question,
            'content': '{"delta":"{\\"ops\\":[{\\"insert\\":\\"Lorem Ipsum\\"},{\\"attributes\\":{\\"align\\":\\"center\\",\\"header\\":1},\\"insert\\":\\"\\\\n\\"},{\\"attributes\\":{\\"italic\\":true},\\"insert\\":\\"\\\\\\"Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...\\\\\\"\\"},{\\"attributes\\":{\\"align\\":\\"center\\",\\"header\\":4},\\"insert\\":\\"\\\\n\\"},{\\"insert\\":\\"\\\\\\"There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...\\\\\\"\\"},{\\"attributes\\":{\\"align\\":\\"center\\",\\"header\\":5},\\"insert\\":\\"\\\\n\\"},{\\"insert\\":\\"\\\\n\\"}]}","html":"<h1 class=\\"ql-align-center\\">Lorem Ipsum</h1><h4 class=\\"ql-align-center\\"><em>\\"Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...\\"</em></h4><h5 class=\\"ql-align-center\\">\\"There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...\\"</h5><p><br></p>"}',
        })

        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        request.user = self.question.user.user
        response = CreateAnswerView.as_view()(request, pk=self.question.id)
        self.assertEqual(response.status_code, 302)

        answer = Answer.objects.all().first()

        self.assertEqual(answer.id, 1)
