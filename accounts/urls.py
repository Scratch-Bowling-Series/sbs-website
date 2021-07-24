from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import RedirectView

from . import views

app_name = 'accounts'

urlpatterns = [
    path('view/<id>/', views.accounts_account_view, name='profile'),
    path('view/add/<id>', views.accounts_add_view, name='add'),
    path('view/remove/<id>', views.accounts_remove_view, name='remove'),
    path('login/', views.accounts_login_view, name='login'),
    path('signup/', views.accounts_signup_view, name='signup'),
    path('logout/', views.accounts_logout_view, name='logout'),
    path('modify/', views.accounts_modify_view, name='modify'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]