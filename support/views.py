from django.shortcuts import render


def support_views(request):
    return render(request, 'main-support.html')