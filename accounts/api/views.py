import io
import json
import os.path

from PIL import Image
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, generics
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from knox.views import LoginView as KnoxLoginView

from ScratchBowling import settings
from ScratchBowling.api.permissions import IsPrivateAllowed
from accounts.api.serializers import UserSerializer, LoginSerializer, SignupSerializer, ProfileSerializer

User = get_user_model()



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # added string
        return super().get_queryset().filter(id=self.request.user.id)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = ProfileSerializer


    permission_classes = [permissions.IsAuthenticated]


class ModifyViewSet(generics.GenericAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user = User.get_user_by_uuid(request.user.id)

        if user:
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.bio = request.data['bio']
            user.email = request.data['email']
            user.setPictureFromRest(request.data['picture'])

            address = request.data['address']
            if address:
                address = json.loads(address)
                if address:
                    if len(address) == 5:
                        user.street = address[0]
                        user.city = address[1]
                        user.state = address[2]
                        user.country = address[3]
                        user.zip = int(address[4] or 0)

            user.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })


class LoginViewSet(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class SignupViewSet(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })






