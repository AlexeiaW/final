import json
from django.test import TestCase,RequestFactory
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *
from django.contrib.auth.models import AnonymousUser, User

from .views import *
from .api import *

class AppUserTest(APITestCase):

    good_url = '/api/images/'

    def test_images_returns_success(self):

        iamge = ImageFactory.create()

        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('id' in data)


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/api/images/')

        # Middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        request.user = AnonymousUser()

        # Test ImageList() as if it were deployed at /api/images/
        response = ImageList(request)
        # Use this syntax for class-based views.
        response = ImageList.as_view()(request)
        self.assertEqual(response.status_code, 200)