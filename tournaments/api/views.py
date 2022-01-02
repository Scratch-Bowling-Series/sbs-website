from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics

from tournaments.api.serializers import TournamentSerializer
from tournaments.models import Tournament, TeamInvite


class TournamentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticated]


class LookingForTeamViewSet(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        friends = []
        if request.user.is_authenticated and 'is_looking' in request.data and 'tournament_id' in request.data:
            success = Tournament.set_looking_for_team(request.data['tournament_id'], request.user.id, request.data['is_looking'])
        return Response({"success": success})

class LeaveTeamViewSet(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        success = False
        if request.user.is_authenticated and 'friend_id' in request.data and 'tournament_id' in request.data:
            success = Tournament.leave_team(request.data['tournament_id'], request.user.id)
        return Response({"success": success})
class SendTeamInviteViewSet(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        success = False
        if request.user.is_authenticated and 'friend_id' in request.data and 'tournament_id' in request.data:
            success = TeamInvite.send_invite(request.data['tournament_id'], request.user.id, request.data['friend_id'])
        return Response({"success": success})
class AcceptTeamInviteViewSet(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        success = False
        if request.user.is_authenticated and 'friend_id' in request.data and 'tournament_id' in request.data:
            success = TeamInvite.accept(request.data['tournament_id'], request.user.id, request.data['friend_id'])
        return Response({"success": success})
class CancelTeamInviteViewSet(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        success = False
        if request.user.is_authenticated and 'friend_id' in request.data and 'tournament_id' in request.data:
            success = TeamInvite.cancel(request.data['tournament_id'], request.user.id, request.data['friend_id'])
        return Response({"success": success})