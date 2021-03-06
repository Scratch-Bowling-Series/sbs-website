import json
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, generics
from knox.models import AuthToken
from rest_framework.response import Response
from ScratchBowling.sbs_utils import is_valid_uuid
from accounts.api.serializers import UserSerializer, LoginSerializer, SignupSerializer, ProfileSerializer, \
    FriendsListSerializer, NotificationSerializer, UserLightSerializer
from accounts.models import Notification

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

class NotificationViewSet(generics.GenericAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        uuid = is_valid_uuid(request.user.id)
        notifications = []
        if uuid:
            queryset = self.get_queryset()
            notifications = queryset.filter(recipient=uuid).order_by('-datetime')

        return Response({
            "notifications": NotificationSerializer(notifications, context=self.get_serializer_context(), many=True).data,
        })

class StorePushTokenViewSet(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        success = False
        queryset = self.get_queryset()
        user = queryset.filter(id=request.user.id).first()
        if user:
            token = request.data['pushToken']
            if token:
                if user.add_push_token(token):
                    print(user.push_tokens)
                    user.save()
                    success = True

        return Response({
            "success": success,
        })

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

class ResendVerifyViewSet(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def get(self, request, *args, **kwargs):
        sent = False
        if request.user.is_authenticated:
            user = User.get_user_by_uuid(request.user.id)
            if user and not user.is_verified:
                user.send_verification_email()
                sent = True
        return Response({
            "success": sent,
        })




class NotificationsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications.all()




class ClearNotificationViewSet(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        success = False
        if request.user.is_authenticated and 'notification_id' in request.data:
            notification_id = request.data['notification_id']
            success = Notification.remove_notification(request.user, notification_id)
        return Response({
            "success": success,
        })


## FRIENDS ##
class FriendsListViewSet(generics.GenericAPIView):
    serializer_class = UserLightSerializer

    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                'friends': UserLightSerializer(request.user.friends.all(), many=True).data,
                'requests_sent' : UserLightSerializer(request.user.friend_requests_sent.all(), many=True).data,
                'requests_received' : UserLightSerializer(request.user.friend_requests_received.all(), many=True).data
            })




class SearchFriendViewSet(generics.GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        friends = []
        if request.user.is_authenticated and 'query' in request.data:
            users, statuses = User.search_friends_extra(request.user.id, request.data['query'])

            if users:
                return Response({"users": UserLightSerializer(users, many=True).data, "statuses": statuses})
        return Response({"users": ''})

class RemoveFriendViewSet(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        success = False
        if request.user.is_authenticated and 'friend_id' in request.data:
            success = User.remove_friend(request.user.id, request.data['friend_id'])
        return Response({"success": success})
class SendFriendRequestViewSet(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        success = False
        if request.user.is_authenticated and 'friend_id' in request.data:
            success = User.send_friend_request(request.user.id, request.data['friend_id'])
        return Response({"success": success})
class AcceptFriendRequestViewSet(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        success = False
        if request.user.is_authenticated and 'friend_id' in request.data:
            success = User.accept_friend_request(request.user.id, request.data['friend_id'])
        return Response({"success": success})
class CancelFriendRequestViewSet(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        success = False
        if request.user.is_authenticated and 'friend_id' in request.data:
            success = User.cancel_friend_request(request.user.id, request.data['friend_id'])
        return Response({"success": success})

