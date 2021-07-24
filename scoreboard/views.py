from django.http import HttpResponse
from django.shortcuts import render

from scoreboard.ranking import run_statistics


def scoreboard(request):
    return HttpResponse(run_statistics())
