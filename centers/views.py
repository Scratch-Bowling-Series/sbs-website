from django.http import Http404
from django.shortcuts import render
from ScratchBowling.pages import create_page_obj
from centers.models import Center


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
                                                         'page': create_page_obj(page, per_page, total_count),
                                                         'page_title': 'Centers',
                                                         'page_description': 'View information about all ' + str(total_count) + ' bowling centers we have held events at.',
                                                         'page_keywords': 'bowling center, business, events, hosting, tournaments, center, lanes'
                                                         })

def single_center_views(request, id):
    center = Center.get_center_by_uuid(id)
    if center:
        total_count = Center.objects.all().count()

        output = [center.center_id, center.center_name, center.center_description]

        return render(request, 'centers/single-center.html', {'nbar': 'centers',
                                                              'center': output,
                                                              'search_type': 'centers_search',
                                                              'page_title': 'Centers',
                                                              'page_description': 'View information about all ' + str(
                                                                 total_count) + ' bowling centers we have held events at.',
                                                              'page_keywords': 'bowling center, business, events, hosting, tournaments, center, lanes'
                                                              })
    else:
        raise Http404('The Center you are looking for does not exist.')


def centers_to_list(centers):
    result = []
    for center in centers:
        result.append([center.center_id,
                       center.center_name,
                       center.location_city,
                       center.location_state,
                       center.phone_number])
    return result