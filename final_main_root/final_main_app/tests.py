import json
from django.test import TestCase, RequestFactory
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


class TestUserCanAddFriends(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        appuser = AppUserFactory.create()
        friend1 = AppUserFactory.create()
        friend2 = AppUserFactory.create()
        self.user = appuser.user
        self.friend1 = friend1
        self.friend2 = friend2

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get(
            '/add-friend/', kwargs={'friend_username': self.friend2.user.username})

        # Add support django messaging framework
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Use this syntax for class-based views.
        response = addFriend(request, self.friend2.user.username)
        self.assertEqual(response.status_code, 200)
