from django.http import HttpRequest
from django.shortcuts import render

from accounts.transfer import Gather
from support.donation import get_donation_count


def support_views(request):

    return render(request, 'main-support.html', {'count': get_donation_count()})