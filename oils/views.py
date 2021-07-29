import json
from django.template.defaulttags import register

from django.shortcuts import render

# Create your views here.
from oils.models import Oil_Pattern
from oils.oil_pattern_scraper import get_oil_colors


@register.filter
def oil_pattern_filter(oil_pattern):
    data = oil_pattern.pattern_cache
    data = json.loads(data)
    return data

def all_patterns_views(request):
    patterns = Oil_Pattern.objects.all()
    data = []
    for pattern in patterns:
        if pattern.pattern_cache is not None and len(pattern.pattern_cache) > 10:
            data.append(pattern)
    oil_colors = get_oil_colors()
    return render(request, 'view-all.html', {'nbar': 'oils', 'oil_patterns': data, 'oil_colors': oil_colors})


def view_pattern_views(request, id):
    return render(request, 'view-all.html', {'nbar': 'oils'})