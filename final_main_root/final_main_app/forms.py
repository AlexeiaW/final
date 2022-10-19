from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')\



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('organisation', 'status')


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'description')


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('title', 'content')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        labels = {
            "name": "Tag"
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.ModelChoiceField(
            queryset=Category.objects.all(), empty_label="Choose a category", label='Category')
