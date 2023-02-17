from ast import And
from django.shortcuts import render
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms.models import model_to_dict
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Count, Sum, F

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
                profile.organisation = profile_form.cleaned_data['organisation']

            if 'status' in user_form.cleaned_data:
                profile.status = profile_form.cleaned_data['status']

            if 'interests' in profile_form.cleaned_data:
                profile.interests.add(*profile_form.cleaned_data['interests'])

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
            
            # Create chat room for the group
            Chat.objects.create(group=group)

            try:
                user_badge = Badge.objects.get(user=appuser)
            except Badge.DoesNotExist:
                badge = Badge.objects.get(name='Group Badge')
                appuser.user_badges.add(badge)
                return render(request, 'my-groups.html', {
                    'badge_unlocked': True,
                    'appuser': request.user.appuser
                })

            messages.success(request,
                             'Your group was successfully created!',
                             extra_tags='alert-success')
            return HttpResponseRedirect('/my-groups/')
    else:
        return render(request, 'create_group.html', {
            'form': GroupForm(),
        })


class CreateStoryView(LoginRequiredMixin, CreateView):
    model = Story()
    form_class = StoryForm
    template_name = 'create_story.html'

    def get_initial(self):
        return {
            'user': self.request.user.appuser.id
        }

    def get_context_data(self, **kwargs):
        context = super(CreateStoryView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['story'] = StoryForm(self.request.POST)
            context['content'] = ContentForm(self.request.POST)
        else:
            context['story'] = StoryForm()
            context['content'] = ContentForm()
        return context

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            context = self.get_context_data()
            content = context['content']

            if content.is_valid() and form.is_valid():
                story = form.save(commit=False)

                story.user = self.request.user.appuser
                story.content = content.save()
                story.author = self.request.user.appuser.author
                story.slug = story.title.lower(
                )

                story.save()

                # assign first story badge to user
                badge = Badge.objects.get(name='Story badge')
                self.request.user.appuser.user_badges.add(badge)

            # save and redirect as usual.
            messages.success(self.request,
                             'Success!',
                             extra_tags='alert-success')
            return super().form_valid(form)
        elif action == 'PREVIEW':
            context = self.get_context_data()
            contentCTX = context['content']
            content = contentCTX.save(commit=False)
            preview = Story(
                category=form.cleaned_data['category'],
                description=form.cleaned_data['description'],
                content=content,
                author=self.request.user.appuser.author,
                title=form.cleaned_data['title'],
                slug=form.cleaned_data['title'].lower()
            )
            ctx = self.get_context_data(preview=preview)
            return self.render_to_response(context=ctx)
        return HttpResponseBadRequest()


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        users_sorted = AppUser.objects.annotate(
            upvote_sum=Sum('user_answers__upvotes')).order_by('-upvote_sum')[:10]

        appuser_object = AppUser.objects.filter(pk=request.user.appuser.id)

        # Maybe weight a story more than likes perhaps (times it by the weight)
        appuser_score = appuser_object.annotate(
            upvote_sum=Sum('user_answers__upvotes'))

        appuser_id = request.user.appuser.id
        rank = None

        for index, item in enumerate(users_sorted):
            if (item.id == appuser_id):
                rank = index + 1

        suggested_users = []
        suggested_stories = []
        suggested_groups = []
        suggested_questions = []
        try:
            # use prefetch here
            # suggest users, stories, groups, questions that are interested in the same categories as the logged in user
            suggested_users = AppUser.objects.filter(
                interests__in=request.user.appuser.interests.all()).exclude(user=request.user).distinct()

            suggested_stories = Story.objects.filter(
                category__in=request.user.appuser.interests.all()).exclude(author__user__user=request.user).distinct()

            suggested_groups = Group.objects.filter(
                category__in=request.user.appuser.interests.all()).exclude(users__user=request.user).distinct()

            suggested_questions = Question.objects.filter(
                category__in=request.user.appuser.interests.all()).exclude(user__user=request.user).distinct()
        except:
            print("An exception occurred")

        return render(request, 'index.html', {
            'appuser': request.user.appuser,
            'users_sorted':  users_sorted,
            'rank': rank,
            'suggested_users': suggested_users,
            'suggested_stories': suggested_stories,
            'suggested_groups': suggested_groups,
            'suggested_questions': suggested_questions,
            'appuser_score': appuser_score
        })


# Render add friends template
def addFriends(request):
    return render(request, 'add_friends.html')


def joinGroupSearch(request):
    return render(request, 'join_group.html')


# Render discover peers template


def discover(request):
    return render(request, 'discover.html')

# Media view, only if login true


@login_required
def media(request):
    return render(request, 'media.html')

# Renders the chat index


def indexChat(request):
    return render(request, 'chat/index.html')

# Renders the room index


@login_required
def room(request, room_name):
    chat = Chat.objects.get(room_id=room_name)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'group': chat.group
    })


def categoryStories(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    stories = category.category_stories.all()
    return render(request, 'category-stories.html', {
        'appuser': request.user.appuser,
        'category': category,
        'stories':  stories,
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
def addReply(request, pk):
    answer = Answer.objects.get(pk=pk)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'index.html')
        reply_form = ReplyForm(data=request.POST)
        content_form = ContentForm(data=request.POST)
        if reply_form.is_valid() and content_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.user = request.user.appuser
            reply.content = content_form.save()
            reply.question = answer.question
            reply.answer = answer
            reply.save()

            messages.success(request,
                             'Your reply was successfully created!',
                             extra_tags='alert-success')
            return HttpResponseRedirect('/question/' + str(answer.question.pk))
    else:
        return render(request, 'add_reply.html', {
            'answer': answer,
            'answer_form': AnswerForm(),
            'content': ContentForm(),
        })


@ login_required
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
        'appuser': request.user.appuser,
        'badge_unlocked': False,
    })


@login_required
def myStories(request):
    # breakpoint()
    return render(request, 'my-stories.html', {
        'appuser': request.user.appuser
    })


@login_required
def exploreStories(request):
    # breakpoint()
    return render(request, 'explore-stories.html', {
        'appuser': request.user.appuser,
        'categories': Category.objects.all(),
        'stories':  Story.objects.all(),
    })


class GroupDetail(DetailView):
    model = Group
    template_name = 'group.html'


class StoryDetail(DetailView):
    model = Story
    template_name = 'story.html'


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
            profile.save()

            if 'organisation' in user_form.cleaned_data:
                profile.organisation = request.DATA['organisation']

            if 'interests' in profile_form.cleaned_data:
                profile.interests.add(*profile_form.cleaned_data['interests'])

            profile.save()

            author = Author(
                user=profile, first_name=profile.user.first_name, last_name=profile.user.last_name)
            author.save()
            profile.author = author
            profile.save()

            registered = True

            # Automatically login the user
            try:
                login(request, user)
                messages.success(request,
                                 'Registration successful!',
                                 extra_tags='alert-success')
                return HttpResponseRedirect('../')
            except:
                print('Unable to automatically log user in.')

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


class AskQuestionView(LoginRequiredMixin, CreateView):
    model = Question()
    form_class = QuestionForm
    template_name = 'ask_question.html'

    def get_initial(self):
        return {
            'user': self.request.user.appuser.id
        }

    def get_context_data(self, **kwargs):
        context = super(AskQuestionView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['question'] = QuestionForm(self.request.POST)
            context['content'] = ContentForm(self.request.POST)
        else:
            context['question'] = QuestionForm()
            context['content'] = ContentForm()
        return context

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            context = self.get_context_data()
            content = context['content']
            if content.is_valid() and form.is_valid():
                question = form.save(commit=False)
                question.user = self.request.user.appuser
                question.content = content.save()
                question.save()
            # save and redirect as usual.
            messages.success(self.request,
                             'Success!',
                             extra_tags='alert-success')
            return super().form_valid(form)
        elif action == 'PREVIEW':
            context = self.get_context_data()
            content = context['content']
            if content.is_valid() and form.is_valid():
                question = form.save(commit=False)
                question.user = self.request.user.appuser
                question.content = content.save(commit=False)

            preview = question
            ctx = self.get_context_data(preview=preview)
            return self.render_to_response(context=ctx)
        return HttpResponseBadRequest()


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question_detail.html'
    second_form_class = QuillFieldForm()

    def get_initial(self):
        return {
            'question': Question.objects.get(pk=self.kwargs['pk']),
            'user': self.request.user.id,
        }

    def get_question(self):
        return Question.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['answer'] = AnswerForm()
        context['content'] = ContentForm()

        return context


class QuestionListView(ListView):
    model = Question
    paginate_by = 100  # if pagination is desired
    template_name = 'question_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def get_queryset(self):
        # order questions by the amount of answers
        questions_sorted = Question.objects.annotate(
            count=Count('answers__id')).order_by('-count')
        return questions_sorted


class CreateAnswerView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'create_answer.html'

    def get_context_data(self, **kwargs):
        context = super(CreateAnswerView, self).get_context_data(
            question=self.get_question(), **kwargs)

        if self.request.POST:
            context['content'] = ContentForm(self.request.POST)
            context['answer'] = AnswerForm(self.request.POST)
        return context

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_valid(self, form):
        action = self.request.POST.get('action')

        # # User should not answer own question
        # if (self.get_question().user.id == self.request.user.appuser.id):
        #     return HttpResponseBadRequest()

        if action == 'SAVE':
            context = self.get_context_data()
            content = context['content']
            if content.is_valid():
                content = content.save()

            answer_form = context['answer']

            if answer_form.is_valid():
                # answer = answer_form.save(commit=False)
                answer = form.save(commit=False)
                answer.content = content
                answer.user = self.request.user.appuser
                answer.question = self.get_question()
                answer.save()

                # assign hub answer badge to user
                badge = Badge.objects.get(name='Hub badge')
                self.request.user.appuser.user_badges.add(badge)

            # save and redirect as usual.
            messages.success(self.request,
                             'Success!',
                             extra_tags='alert-success')
            # save and redirect as usual.
            return super().form_valid(form)
        elif action == 'PREVIEW':
            ctx = self.get_context_data(preview=form.cleaned_data['answer'])
            return self.render_to_response(context=ctx)
        return HttpResponseBadRequest()

    def get_question(self):
        return Question.objects.get(pk=self.kwargs['pk'])
