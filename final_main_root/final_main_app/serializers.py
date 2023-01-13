from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'email', 'date_joined']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['name', 'image', 'thumbnail']


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['name', 'image', 'thumbnail']


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class StoryListSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%d-%m-%Y")

    class Meta:
        model = Story
        fields = ["pk", "author", "category", "created_on",
                  "description", "slug", "title", "updated_on"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["author"] = AuthorSerializer(instance.author).data
        data["category"] = CategorySerializer(instance.category).data
        return data


class QuestionListSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%b. %d, %Y")

    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = AppUserSerializer(instance.user).data
        data["content"] = ContentSerializer(instance.content).data
        # data["answers"] = AnswerSerializer(instance.answers).data
        return data


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class AppUserSerializer(serializers.ModelSerializer):
    user = User

    class Meta:
        model = AppUser
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = UserSerializer(instance.user).data
        # data["images"] = ImageListSerializer(instance.images).data
        data["image"] = ImageListSerializer(instance.images.first()).data
        # breakpoint()
        return data


class HomePagesAppUserSerializer(serializers.ModelSerializer):
    user = User()

    class Meta:
        model = AppUser
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = UserSerializer(instance.user).data
        return data


class AnswerSerializer(serializers.ModelSerializer):
    user = AppUser()
    question = Question()
    content = Content()

    class Meta:
        model = Answer
        fields = '__all__'
