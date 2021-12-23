from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views as rest_views

import accounts
from . import views, shortener
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from accounts.api.urls import router as accounts_router
from tournaments.api.urls import router as tournaments_router
from .api.token import CustomAuthToken

accounts_router.registry.extend(tournaments_router.registry)
router = accounts_router

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
    path('help-center/', views.help_center, name='help-center'),
    path('faqs/', views.help_center, name='faqs'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('live-chat/', views.live_chat, name='live-chat'),
    path('contact/', views.contact, name='contact'),
    path('merch/', include('merch.urls')),
    path('oil-patterns/', include('oils.urls')),
    path('about/', views.about, name='about'),
    path('prolink/', include('prolink.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('scrape/tournaments/', views.scrape_tournaments, name='scrape_tournaments'),
    path('scrape/bowlers/', views.scrape_bowlers, name='scrape_bowlers'),
    path('search/', views.search, name='search'),

    path('api/', include(router.urls)),
    path('api/user/', include(accounts.api.urls)),


    ## URL SHORTENER
    path('s/<code>/', shortener.shorten, name='shortener'),
    path('s/create/new/<url>/', shortener.create, name='shortener')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
