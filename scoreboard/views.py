from django.http import HttpResponse
from django.shortcuts import render


def scoreboard(request):
    data = {'test':None}
    return render(request, 'scoreboard/scoreboard.html', data)
