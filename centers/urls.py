from django.urls import include, path
from . import views

app_name = 'centers'

urlpatterns = [
    path('', views.centers_views, name='centers'),
    path('page/<page>', views.centers_views, name='centers'),

    path('view/<id>', views.single_center_views, name='center')
]
