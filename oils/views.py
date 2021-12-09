from django.shortcuts import render

from oils.models import Oil_Pattern
from oils.oil_pattern_scraper import get_oil_colors


def all_patterns_views(request, amount=20, offset=0):
    meta = {'nbar': 'oils',}
    data = {'oil_patterns': Oil_Pattern.get_all_patterns_converted(amount, offset),
            'oil_colors': get_oil_colors()}
    return render(request, 'view-all.html', meta | data)

def single_pattern_views(request, id):
    meta = {'nbar': 'oils', }
    data = {'oil_patterns': Oil_Pattern.get_oil_pattern_converted_uuid(id),
            'oil_colors': get_oil_colors()}
    return render(request, 'view-single.html', meta | data)