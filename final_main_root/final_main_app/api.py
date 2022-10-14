from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from .tasks import *
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins, filters

@api_view(['GET'])
def helloworld(request, **kwargs):
    if request.method == 'GET':
        return Response({'coverage': 'hi'}, status=status.HTTP_200_OK)

# Get an individual image
class ImageDetail(mixins.CreateModelMixin,  generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        appuser = self.request.user.appuser
        record = serializer.save(user=appuser)
        make_thumbnail.delay(record.pk, appuser.pk)

    def create(self, request, *args, **kwargs):
        response = super(ImageDetail, self).create(request, *args, **kwargs)
        return HttpResponseRedirect(redirect_to='/media')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Get a list of images
class ImageList(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageListSerializer

    def get_queryset(self):
            """
            Restricts the returned iamges to a given user,
            by filtering against a `user` in request.
            """
            queryset =  self.request.user.appuser.images
            return queryset

# Get a list of users through api, based on search criteria from the client. The search will be based on the username
class UsersAPIView(generics.ListCreateAPIView):
    serializer_class = AppUserSerializer
    def get_queryset(self):
            """
            Optionally restricts the returned a given user,
            by filtering against a `username` query parameter in the URL.
            """
            queryset = AppUser.objects.all()
            username = self.request.query_params.get('username')
            if username is not None:
                queryset = queryset.filter(user__username__icontains=username)
            return queryset

# Get a list of all the users in the system as an array of json objects
class AllUsersAPIView(generics.ListCreateAPIView):
    serializer_class = HomePagesAppUserSerializer
    queryset = AppUser.objects.all()
