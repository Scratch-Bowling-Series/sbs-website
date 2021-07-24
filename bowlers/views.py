from django.shortcuts import render

def bowlers_views(request):
    return render(request, 'bowlers/main-bowlers.html', {'nbar': 'bowlers'})
