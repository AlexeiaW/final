# from asyncio.windows_events import NULL
from email.policy import default
from queue import Empty
import re
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
import uuid
from django_quill.fields import QuillField
from django.urls.base import reverse
# The Model that is used to add data to the auth user model. AppUser is mainly used as the "user" and will create relationships between friends


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    slug = models.SlugField(null=True, blank=True, default=None, db_index=True)

    def __str__(self):
        return self.name


class Content(models.Model):
    content = QuillField()
    created_on = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    organisation = models.CharField(max_length=256, null=True, blank=True)
    status = models.TextField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    friends = models.ManyToManyField(
        "self",
        related_name="appuser_friends",
        symmetrical=False,
        blank=True
    )

    interests = models.ManyToManyField(
        Category, related_name='categories_appusers')

    def __str__(self):
        return self.user.username

# Image model to store image information


class Image(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)
    image = models.FileField(blank=False)
    thumbnail = models.FileField(null=True)
    user = models.ForeignKey(
        AppUser, related_name='images', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

# Group model to store user groups


class Group(models.Model):
    name = models.CharField(max_length=30, unique=False, db_index=True)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(AppUser, related_name='groups')
    created_on = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='category_groups', null=True)

    def __str__(self):
        return self.name


class Chat(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    # This field is universally unique, and will ensure chat rooms are unique for those who create them
    room_id = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False)

    def __str__(self):
        return self.room_id.hex


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name


class Story(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='author_stories')
    updated_on = models.DateTimeField(auto_now=True)
    # content = QuillField()
    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='category_stories', null=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('final_main_app:story_detail', kwargs={'pk': self.id})


class Question(models.Model):
    title = models.CharField(max_length=140)
    # question = QuillField()
    content = models.OneToOneField(Content, on_delete=models.CASCADE)

    user = models.ForeignKey(AppUser,
                             on_delete=models.CASCADE, related_name='appuser_questions')
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='category_questions', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('final_main_app:question_detail', kwargs={'pk': self.id})


class Answer(models.Model):
    # answer = QuillField()
    content = models.OneToOneField(Content, on_delete=models.CASCADE)

    user = models.ForeignKey(AppUser, related_name='user_answers',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(to=Question, related_name='answers',
                                 on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    replies = models.ManyToManyField(
        "self",
        related_name="answer_replies",
        symmetrical=False,
        blank=True
    )

    class Meta:
        ordering = ('-created', )
