from django.shortcuts import render

from support.donation_count import set_count, get_count


def support_views(request):
    return render(request, 'main-support.html', {'count': get_count()})