from django.urls import include, path
from . import views
from . import api
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', login_required(login_url='../login/')
         (views.appuserUpdate), name='appuser_update'),
    path('discover/', login_required(login_url='../login/')
         (views.discover), name='discover'),
    path('profile/', views.profile, name='profile'),
    path('friends/', views.friends, name='profile'),
    path('groups/', views.groups, name='groups'),
    path('join-group-search/', views.joinGroupSearch, name='join_group'),
    path('reset-password/', views.resetPassword, name='resetPassword'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('api/image/', api.ImageDetail.as_view(), name="image_api"),
    path('api/images/', api.ImageList.as_view(), name="images_api"),
    path('api/search-users/', api.UsersAPIView.as_view(),
         name='search_groups_api'),
    path('api/search-groups/', api.GroupsAPIView.as_view(),
         name='search_groups_api'),
    path('api/users/all/', api.AllUsersAPIView.as_view(), name='all_users_api'),
    path('media/',  login_required(login_url='../login/')
         (views.media), name='media'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('new-chat/', views.indexChat, name='indexChat'),
    path('add-friends/', views.addFriends, name='add_friends'),
    path('add-friend/<str:friend_username>/',
         login_required(login_url='../login/')(views.addFriend), name='add_friend'),
    path('join-group/<str:group_name>/',
         login_required(login_url='../login/')(views.joinGroup), name='join_group'),
    path('my-friends/', login_required(login_url='../login/')
         (views.myFriends), name='my_friends'),
    path('my-groups/', login_required(login_url='../login/')
         (views.myGroups), name='my_groups'),
    path('group/<int:pk>', views.GroupDetail.as_view(), name='group'),
    path('create-group/', views.createGroup, name='create_group'),
    path('create-story/', views.createStory, name='create_story'),
    path('stories-index/', views.storiesIndex, name='create_index'),

]
