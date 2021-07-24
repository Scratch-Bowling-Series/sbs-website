from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.index, name='index'),
    path('tournaments/', include('tournaments.urls')),
    path('bowlers/', include('bowlers.urls')),
    path('centers/', include('centers.urls')),
    path('scoreboard/', include('scoreboard.urls')),
    path('broadcasts/', include('broadcasts.urls')),
    path('support/', include('support.urls')),
    path('merch/', include('merch.urls')),
    path('about/', views.about, name='about'),

    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
