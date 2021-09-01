import datetime

from django.shortcuts import render

from ScratchBowling.pages import create_page_obj
from centers.models import Center
from tournaments.models import Tournament


def centers_views(request, page=1):
    page = int(page)
    per_page = 40
    centers = Center.objects.all()
    total_count = len(centers)
    start = (per_page * page) - per_page
    end = per_page * page
    centers = centers[start:end]
    return render(request, 'centers/main-centers.html', {'nbar': 'centers',
                                                         'centers': centers_to_list(centers),
                                                         'total_centers': total_count,
                                                         'search_type': 'centers_search',
                                                         'page': create_page_obj(page, per_page, total_count)})



def centers_to_list(centers):
    result = []
    for center in centers:
        result.append([center.center_id,
                       center.center_name,
                       center.location_city,
                       center.location_state,
                       center.phone_number])
    return result