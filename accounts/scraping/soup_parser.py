import io
import os
import random

import requests
from PIL import Image

from ScratchBowling import settings
from ScratchBowling.sbs_utils import normalize_state


def update_user_with_soup(user, soup):
    first, last = get_name(soup)
    city, state = get_location(soup)
    email = first + last + '-' + city + str(random.randrange(0,1000)) + '@temp.com'
    image = get_image(soup, email)

    if first:
        user.email = email
        user.first_name = first
        user.last_name = last
        user.location_city = city
        user.location_state = state
        user.picture = image
        return True
    return False


def get_name(soup):
    first = ''
    last = ''
    tag = soup.find(class_="field field--name-title field--type-string field--label-hidden")
    if tag:
        full_name = tag.text
        if full_name:
            if '(' in full_name:
                full_name = full_name.split('(', 1)[0]
            full_name = full_name.split(' ', 1)
            length = len(full_name)
            if length > 1:
                first = full_name[0]
                last = full_name[1]
            elif length == 1:
                first = full_name[0]
    return first, last

def get_location(soup):
    city = ''
    state = ''
    tag = soup.find(class_="col-sm-3")
    if tag:
        tag = tag.find(class_='field__item')
        if tag:
            location = tag.text
            if location:
                locations = location.split(',', 1)
                if len(locations) > 1:
                    city = locations[0]
                    state = normalize_state(locations[1])
    return city, state

def get_image(soup, email):
    path = ''
    tag = soup.find(class_='image-style-bio')
    if tag:
        url = tag.get('src')
        if url:
            response = requests.get('https://scratchbowling.com' + str(url))
            original = Image.open(io.BytesIO(response.content))
            if original:
                path = 'profile-pictures/' + str(email) + '.png'
                original.save(os.path.join(settings.MEDIA_ROOT, path))
    return path