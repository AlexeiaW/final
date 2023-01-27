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


class ContentFactory(factory.django.DjangoModelFactory):
    content = '{"delta":"{\\"ops\\":[{\\"insert\\":\\"Lorem Ipsum\\"},{\\"attributes\\":{\\"align\\":\\"center\\",\\"header\\":1},\\"insert\\":\\"\\\\n\\"},{\\"attributes\\":{\\"italic\\":true},\\"insert\\":\\"\\\\\\"Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...\\\\\\"\\"},{\\"attributes\\":{\\"align\\":\\"center\\",\\"header\\":4},\\"insert\\":\\"\\\\n\\"},{\\"insert\\":\\"\\\\\\"There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...\\\\\\"\\"},{\\"attributes\\":{\\"align\\":\\"center\\",\\"header\\":5},\\"insert\\":\\"\\\\n\\"},{\\"insert\\":\\"\\\\n\\"}]}","html":"<h1 class=\\"ql-align-center\\">Lorem Ipsum</h1><h4 class=\\"ql-align-center\\"><em>\\"Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...\\"</em></h4><h5 class=\\"ql-align-center\\">\\"There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...\\"</h5><p><br></p>"}'

    class Meta:
        model = Content


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


class QuestionFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(AppUserFactory)
    category = factory.SubFactory(CategoryFactory)
    content = factory.SubFactory(ContentFactory)
    title = 'Some question title'

    class Meta:
        model = Question


class ImageFactory(factory.django.DjangoModelFactory):
    name = models.CharField(max_length=256, unique=True, db_index=True)
    image = factory.django.ImageField(
        from_path='images/test.jpg')
    thumbnail = factory.django.ImageField(
        from_path='images/test.jpg')

    user = factory.SubFactory(AppUserFactory)

    class Meta:
        model = Image
