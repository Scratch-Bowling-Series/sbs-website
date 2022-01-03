from django.conf.urls import url

from rest_framework import routers
from knox import views as knox_views
from accounts.api import views

router = routers.DefaultRouter()


router.register(r'user/data', views.UserViewSet, basename='user-data')
router.register(r'user/profile', views.ProfileViewSet, basename='profile-data')
router.register(r'user/notifications', views.NotificationsViewSet, basename='notifications')

urlpatterns = [
    url(r'resend-verify-email/', views.ResendVerifyViewSet.as_view(), name='resend-verify-email'),

    url(r'clear-notification/', views.ClearNotificationViewSet.as_view(), name='clear-notification'),
    url(r'store-push/', views.StorePushTokenViewSet.as_view(), name='store-push'),


    url(r'friend/list/', views.FriendsListViewSet.as_view(), name='friends-list'),
    url(r'friend/search/', views.SearchFriendViewSet.as_view(), name='search-friend'),
    url(r'friend/remove/', views.RemoveFriendViewSet.as_view(), name='remove-friend'),
    url(r'friend/send-request/', views.SendFriendRequestViewSet.as_view(), name='send-friend-request'),
    url(r'friend/accept-request/', views.AcceptFriendRequestViewSet.as_view(), name='accept-friend-request'),
    url(r'friend/cancel-request/', views.CancelFriendRequestViewSet.as_view(), name='cancel-friend-request'),

    url(r'modify/',  views.ModifyViewSet.as_view(), name='modify'),
    url(r'login/', views.LoginViewSet.as_view(), name='login'),
    url(r'signup/', views.SignupViewSet.as_view(), name='signup'),
    url(r'logout/', knox_views.LogoutView.as_view(), name='logout'),
    url(r'logout-all/', knox_views.LogoutAllView.as_view(), name='logout_all')
]