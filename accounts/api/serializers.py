from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.core import exceptions
import django.contrib.auth.password_validation as validators

from accounts.models import Notification

User = get_user_model()


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'sender', 'datetime', 'title', 'body', 'type', 'read', 'data']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    has_notifications = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'bio', 'picture', 'city', 'state', 'street', 'zip', 'country', 'has_notifications']

class UserLightSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'picture']

class FriendsListSerializer(serializers.ModelSerializer):
    friends = UserLightSerializer(source='friends_objects', many=True, read_only=True)
    sent = UserLightSerializer(source='friends_outbound_objects', many=True, read_only=True)
    requests = UserLightSerializer(source='friends_inbound_objects', many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'friends', 'requests', 'sent']







class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'bio', 'picture', 'city', 'state']



class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email','first_name', 'last_name', 'password', 'city', 'state')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, password):
        errors = []
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return password


    def create(self, validated_data):
        first_name = ''
        last_name = ''
        if 'first_name' in validated_data:
            first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            last_name = validated_data['last_name']

        user = User.objects.create_user(
            validated_data['email'],
            validated_data['password'],
            first_name or '',
            last_name or ''
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")