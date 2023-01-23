import factory
from random import randint
from random import choice

from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *
from django.contrib.auth.models import User
import random
import string


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = '1234'

    class Meta:
        model = User


class CategoryFactory(factory.django.DjangoModelFactory):
    slug = factory.Faker('word')
    name = slug

    class Meta:
        model = Category


class AppUserFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    organisation = 'Google'

    status = 'Some status content'

    class Meta:
        model = AppUser

    @factory.post_generation
    def friends(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for friends in extracted:
                self.friends.add(friends)


class ImageFactory(factory.django.DjangoModelFactory):
    name = models.CharField(max_length=256, unique=True, db_index=True)
    image = factory.django.ImageField(
        from_path='images/test.jpg')
    thumbnail = factory.django.ImageField(
        from_path='images/test.jpg')

    user = factory.SubFactory(AppUserFactory)

    class Meta:
        model = Image
