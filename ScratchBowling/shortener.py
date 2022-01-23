import random
import string

from django.http import HttpResponse, HttpResponseRedirect, Http404

from accounts.models import Shorten


def shorten(request, code):
    if code == '' or len(code) != 5:
        return Http404('This link is broken...')
    shorten = Shorten.objects.filter(code=code).first()
    if shorten != None:
        return HttpResponseRedirect(shorten.url)
    return Http404('This link is broken...')

def create(request, url):
    if url == '' or len(url) < 5:
        return HttpResponse('')
    else:
        return HttpResponse(create_link(url))



def create_link(link):
    link = link.replace('&sl', '/')
    shorten = Shorten.objects.filter(url=link).first()
    if shorten != None:
        return 'https://www.bowl.sbs/s/' + str(shorten.code) + '/'
    else:
        code = generate_code()
        if code == None: return None
        shorten = Shorten()
        shorten.code = code
        shorten.url = link
        shorten.save()
        return 'https://www.bowl.sbs/s/' + str(shorten.code) + '/'

def generate_code():
    for x in range(0, 100):
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        if Shorten.objects.filter(code=code).first() == None:
            return code
    return None