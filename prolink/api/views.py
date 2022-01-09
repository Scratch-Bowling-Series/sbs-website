from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics

from prolink.api.serializers import TransactionSerializer, DrawerSerializer, UserDrawerSerializer
from prolink.models import Drawer

User = get_user_model()


class DrawerTransactionsViewSet(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        drawer = None
        if request.user.is_authenticated and request.user.is_staff:
            drawer = Drawer.get_open_drawer(request.user)
        return Response({
            "drawer": DrawerSerializer(drawer, context={'request':request}).data
        })
class AllOpenDrawersViewset(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        drawers = []
        if request.user.is_authenticated and request.user.is_staff and request.user.is_drawer_manager:
            drawers = Drawer.objects.filter(opened=True)
        return Response({
            "drawers": DrawerSerializer(drawers, many=True).data,
        })

class UserDrawerViewset(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        print(request.user.is_authenticated)
        user = None
        if request.user.is_authenticated and request.user.is_staff:
            if 'user_id' in request.data:
                user = User.get_user_by_uuid(request.data['user_id'])
        return Response({
            "user": UserDrawerSerializer(user, context={'request':request}).data,
        })

class DrawerTransactionViewset(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        success = False
        transaction = None
        if request.user.is_authenticated and request.user.is_staff:
            if 'user_id' in request.data and 'amount' in request.data:
                owner = User.get_user_by_uuid(request.user.id)
                user = User.get_user_by_uuid(request.data['user_id'])
                if user and owner:
                    transaction = Drawer.make_transaction(owner, user, request.data['amount'])
                    if transaction:
                        success = True
        return Response({
            "success": success,
            "user": UserDrawerSerializer(user, context={'request':request}).data
        })

