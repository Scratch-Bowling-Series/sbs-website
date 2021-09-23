from django.shortcuts import render
from support.donation import get_donation_count


def support_views(request):
    return render(request, 'main-support.html', {'count': get_donation_count(),
                                                 'page_title': 'Support Us',
                                                 'page_description': "Thank you to everyone that helped us hit our most recent goal. Check out what's to come here.",
                                                 'page_keywords': 'support, donation, fundraiser, help, raise, goals, contributions, subscribe'
                                                 })