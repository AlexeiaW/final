from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    # interest = forms.ModelChoiceField(queryset=Category.objects.all(
    # ), empty_label="Choose what interests you", label='Interests')
    # categories = Category.objects.all()
    # interest = forms.ModelMultipleChoiceField(
    #     widget=forms.CheckboxSelectMultiple, required=True, queryset=categories, label='Interests')
    interests = forms.ModelMultipleChoiceField(
        Category.objects.all(), widget=forms.SelectMultiple)

    class Meta:
        model = AppUser
        fields = ('organisation', 'status', 'description', 'interests')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class StoryForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(
    ), empty_label="Choose a category", label='Category')

    class Meta:
        model = Story
        fields = ('title', 'description', 'content', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class QuestionForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=AppUser.objects.all(),
        disabled=True,
    )

    class Meta:
        model = Question
        fields = ['title', 'question', 'user', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class AnswerForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=AppUser.objects.all(),
        disabled=True,
    )
    question = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Question.objects.all(),
        disabled=True,
    )

    class Meta:
        model = Answer
        fields = ['answer', 'user', 'question', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
