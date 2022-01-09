from django.conf.urls import url
from rest_framework import routers

from prolink.api import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'drawer/self/', views.DrawerTransactionsViewSet.as_view(), name='drawer-self'),
    url(r'drawer/view-user/', views.UserDrawerViewset.as_view(), name='drawer-view'),
    url(r'drawer/all-open/', views.AllOpenDrawersViewset.as_view(), name='drawers-open'),
    url(r'drawer/transaction/', views.DrawerTransactionViewset.as_view(), name='transaction'),
]