from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views, shortener
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.index, name='index'),
    path('notify/<notify>/', views.index, name='notify'),
    path('tournaments/', include('tournaments.urls')),
    path('bowlers/', include('bowlers.urls')),
    path('centers/', include('centers.urls')),
    path('vods/', include('vods.urls')),
    path('scoreboard/', include('scoreboard.urls')),
    path('broadcasts/', include('broadcasts.urls')),
    path('support/', include('support.urls')),
    path('contact/', views.contact, name='contact'),
    path('merch/', include('merch.urls')),
    path('oil-patterns/', include('oils.urls')),
    path('about/', views.about, name='about'),
    path('prolink/', include('prolink.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('get-last-commit/', views.has_content_changed),
    path('scrape/tournaments/', views.scrape_tournaments, name='scrape_tournaments'),
    path('scrape/bowlers/', views.scrape_bowlers, name='scrape_bowlers'),
    path('search/', views.search, name='search'),



    ## URL SHORTENER
    path('s/<code>/', shortener.shorten, name='shortener'),
    path('s/create/new/<url>/', shortener.create, name='shortener')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
