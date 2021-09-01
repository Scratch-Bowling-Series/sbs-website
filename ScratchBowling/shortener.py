import random
import string

from accounts.models import Shorten


def create_link(link):
    link = link.replace('&sl', '/')
    shorten = Shorten.objects.filter(url=link).first()
    if shorten != None:
        return 'https://scratchbowling.pythonanywhere.com/s/' + str(shorten.code) + '/'
    else:
        code = generate_code()
        if code == None: return None
        shorten = Shorten()
        shorten.code = code
        shorten.url = link
        shorten.save()
        return 'https://scratchbowling.pythonanywhere.com/s/' + str(shorten.code) + '/'


def generate_code():
    for x in range(0, 100):
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        if Shorten.objects.filter(code=code).first() == None:
            return code
    return None