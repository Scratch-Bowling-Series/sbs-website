from django.shortcuts import render

def broadcasts_views(request):
    return render(request, 'broadcasts/main-broadcasts.html', {'nbar': 'broadcasts'})
