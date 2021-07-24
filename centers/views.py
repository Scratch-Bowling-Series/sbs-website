import datetime

from django.shortcuts import render

from tournaments.models import Tournament


def centers_views(request):
    return render(request, 'centers/main-centers.html', {'nbar': 'centers'})
