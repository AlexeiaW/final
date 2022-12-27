import json
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *
from django.contrib.auth.models import AnonymousUser, User

from .views import *
from .api import *
from .models import *
from django.contrib.messages.storage.fallback import FallbackStorage


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

        # Use this syntax for class-based views.
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
