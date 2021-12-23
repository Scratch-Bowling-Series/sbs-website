from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from knox import views as knox_views
from accounts.api import views

router = routers.DefaultRouter()


router.register(r'user/data', views.UserViewSet, basename='user-data')
router.register(r'profile', views.ProfileViewSet, basename='profile-data')

urlpatterns = [
    url(r'modify/',  views.ModifyViewSet.as_view(), name='modify'),
    url(r'login/', views.LoginViewSet.as_view(), name='login'),
    url(r'signup/', views.SignupViewSet.as_view(), name='signup'),
    url(r'logout/', knox_views.LogoutView.as_view(), name='logout'),
    url(r'logout-all/', knox_views.LogoutAllView.as_view(), name='logout_all')
]