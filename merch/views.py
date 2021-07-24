from django.shortcuts import render

def merch_views(request):
    return render(request, 'merch/main-merch.html', {'nbar': 'merch'})
