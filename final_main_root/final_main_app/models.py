from django.db import models
from django.contrib.auth.models import User

# The Model that is used to add data to the auth user model. AppUser is mainly used as the "user" and will create relationships between friends


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    organisation = models.CharField(max_length=256, null=True, blank=True)

    status = models.TextField(null=True, blank=True)

    friends = models.ManyToManyField(
        "self",
        related_name="appuser_friends",
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.user.username

# Image model to store image information


class Image(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)
    image = models.FileField(blank=False)
    thumbnail = models.FileField(null=True)
    user = models.ForeignKey(
        AppUser, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Group model to store user groups


class Group(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    user = models.ManyToManyField(AppUser)

    def __str__(self):
        return self.name


class Chat(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
