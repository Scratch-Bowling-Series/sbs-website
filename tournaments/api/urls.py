from django.conf.urls import url
from rest_framework import routers

from tournaments.api import views

router = routers.DefaultRouter()
router.register(r'tournament/all', views.TournamentViewSet, basename='all-tournaments')

urlpatterns = [
    url(r'team/looking-for-team/', views.LookingForTeamViewSet.as_view(), name='looking-for-team'),
    url(r'team/leave/', views.LeaveTeamViewSet.as_view(), name='leave-team'),
    url(r'team/send-invite/', views.SendTeamInviteViewSet.as_view(), name='send-team-invite'),
    url(r'team/accept-invite/', views.AcceptTeamInviteViewSet.as_view(), name='accept-team-invite'),
    url(r'team/cancel-invite/', views.CancelTeamInviteViewSet.as_view(), name='cancel-team-invite'),
]