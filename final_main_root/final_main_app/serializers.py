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
        fields = ['name', 'image']


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['name', 'image', 'thumbnail']


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class AppUserSerializer(serializers.ModelSerializer):
    user = User

    class Meta:
        model = AppUser
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = UserSerializer(instance.user).data
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
