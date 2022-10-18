from ast import And
from django.shortcuts import render
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms.models import model_to_dict

# Update user


def appuserUpdate(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST, instance=request.user)
        profile_form = UserProfileForm(
            data=request.POST, instance=request.user.appuser)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'organisation' in user_form.cleaned_data:
                profile.organisation = request.DATA['organisation']

            if 'status' in user_form.cleaned_data:
                profile.staus = request.DATA['status']

            profile.save()
            return HttpResponseRedirect('../')
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserUpdateForm(initial=model_to_dict(request.user))
        profile_form = UserProfileForm(
            initial=model_to_dict(request.user.appuser))

    return render(request, 'appuser_update_form.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def createGroup(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'index.html')

        form = GroupForm(data=request.POST)
        if form.is_valid():
            groupForm = form.save()

            appuser = AppUser.objects.get(id=request.user.appuser.id)

            # This is the group the authenticated user wants to connect with
            group = Group.objects.get(pk=groupForm.pk)

            appuser.groups.add(group)
            appuser.save()

            messages.success(request,
                             'Your group was successfully created!',
                             extra_tags='alert-success')
            return HttpResponseRedirect('/my-groups/')
    else:
        return render(request, 'create_group.html', {
            'form': GroupForm(),
        })


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'index.html', {
            'appuser': request.user.appuser
        })


# Render add friends template
def addFriends(request):
    return render(request, 'add_friends.html')


def joinGroupSearch(request):
    return render(request, 'join_group.html')


# Render discover peers template


def discover(request):
    return render(request, 'discover.html')


def profile(request):
    return render(request, 'profile.html')


def friends(request):
    return render(request, 'friends.html')


def groups(request):
    return render(request, 'groups.html')
# Media view, only if login true


@login_required
def media(request):
    return render(request, 'media.html')

# Renders the chat index


def indexChat(request):
    return render(request, 'chat/index.html')

# Renders the room index


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

# Add friend endpoint to associate friends with each other


@login_required
def addFriend(request, friend_username):
    # This is the authenticated user, who is initiating the friend connection
    appuser = request.user.appuser

    # This is the friend the authenticated user wants to connect with
    friend = AppUser.objects.get(user__username__exact=friend_username)
    appuser.friends.add(friend)
    appuser.save()

    messages.success(request,
                     'Friend successfully added!',
                     extra_tags='alert-success')

    return HttpResponseRedirect('/my-friends/')


@login_required
def joinGroup(request, group_name):
    # This is the authenticated user, who is initiating the group connection
    appuser = AppUser.objects.get(id=request.user.appuser.id)

    # This is the group the authenticated user wants to connect with
    group = Group.objects.get(name__exact=group_name)

    appuser.groups.add(group)
    appuser.save()

    messages.success(request,
                     'Group successfully joined!',
                     extra_tags='alert-success')

    return HttpResponseRedirect('/my-groups/')

# Returns a list of user friends


@login_required
def myFriends(request):
    return render(request, 'my-friends.html', {
        'appuser': request.user.appuser
    })


@login_required
def myGroups(request):
    return render(request, 'my-groups.html', {
        'appuser': request.user.appuser
    })


# Password change view, render password change form and process submission of the form


def resetPassword(request):
    """View function for the user profile, profile.html."""
    # Get the current user's user object
    # user = request.user
    # # Look-up the username in the database
    # current_user_name = User.objects.get(username=user.username)
    # current_user_avatar = UserProfile.objects.get(user=user.id)
    # If ths is a POST, process it as a password update
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # This is a VERY important step!
            update_session_auth_hash(request, user)
            messages.success(request,
                             'Your password was successfully updated!',
                             extra_tags='alert-success')
            return HttpResponseRedirect('../')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'reset_password.html', {
        'form': form,
        # 'current_user': current_user_name,
        # 'user_avatar': current_user_avatar
    })


# Register view, register form and process form submission


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'organisation' in user_form.cleaned_data:
                profile.organisation = request.DATA['organisation']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


# Login form and process form submission
def user_login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                messages.success(request,
                                 'Login successful!',
                                 extra_tags='alert-success')
                return HttpResponseRedirect('../')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html', {})

# Process user logout


@login_required
def user_logout(request):
    logout(request)
    messages.success(request,
                     'Logout successful!',
                     extra_tags='alert-success')
    return HttpResponseRedirect('../')
