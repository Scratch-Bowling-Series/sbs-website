from rest_framework import viewsets, permissions

from tournaments.api.serializers import TournamentSerializer
from tournaments.models import Tournament


class TournamentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticated]