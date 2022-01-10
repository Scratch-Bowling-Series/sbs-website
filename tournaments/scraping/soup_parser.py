from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from pytz import timezone

from centers.models import Center


User = get_user_model()

def update_tournament_with_soup(tournament, soup):
    name = get_name(soup)
    if name:
        tournament.name = name

    date_time = get_datetime(soup)
    if date_time:
        tournament.datetime = date_time

    center_id = get_center(soup)
    if center_id:
        tournament.center_id = center_id

    ##get_game_data(tournament, soup)

    entry = get_entry(soup)
    if entry:
        tournament.entry_fee = entry

    desc = get_description(soup)
    if desc:
        tournament.description = desc

    oil_pattern_id = get_oil(soup)
    if oil_pattern_id:
        tournament.oil_pattern_id = oil_pattern_id

    #picture = get_image(soup)
    #if picture:
    #    tournament.picture = picture


    return True

def get_name(soup):
    title = soup.find(class_='field field--name-title field--type-string field--label-hidden')
    if title is not None:
        if '-' in title.text:
            return title.text.split('-')[1]
        else:
            return title.text
    return None

def get_entry(soup):
    title = soup.find(class_='field field--name-field-entry-fee field--type-string field--label-inline')
    if title is not None:
        entry = title.find(class_='field__item')
        if entry:
            entry = entry.text
            entry = entry.replace("$","")
            if '-' in entry:
                entry = entry.split('-')[0]
            if '/' in entry:
                entry = entry.split('/')
                entry = entry[0]
            if entry:
                try:
                    return int(entry)
                except ValueError:
                    return 0
    return 0

def get_description(soup):
    desc = soup.find(class_='field--type-text-with-summary')
    if desc != None:
        desc = soup.find('p')
        if desc != None:
            return desc.text
    return None

def get_datetime(soup):
    time = soup.find('time')
    if time:
        time = time['datetime']
        time += ' -0500'
        return datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ %z')
    return None

def get_center(soup):
    title = soup.find(class_='field field--name-field-bowling-center field--type-entity-reference field--label-inline')
    if title:
        tag = title.find('a')
        if tag:
            url = tag.get('href')
            if url and '/bowling-center/' in url:
                base_url = 'https://scratchbowling.com'
                url = base_url + url
                center = Center.objects.filter(soup_url=url).first()
                if center:
                    return center.center_id
    return None

# def get_qualifiers(soup):
#     tables = soup.find(id="qualifying-1")
#     if tables is not None:
#         placements = []
#         if tables is not None:
#             rows = tables.find_all('tr')
#             if rows is not None:
#                 first = 0
#                 for row in rows:
#                     first = first + 1
#                     if first != 1:
#                         if row is not None:
#                             if row.children is not None:
#                                 count = 0
#                                 data = []
#                                 for item in row.children:
#                                     count = count + 1
#                                     if count == 4:
#                                         name = row.find('a', href=True, text=True)
#                                         if name is not None and name['href'] is not None:
#                                             data.append(name['href'])
#                                     elif item.string != '\n':
#                                         data.append(item.string)
#                                 placements.append(data)
#
#         for placement in placements:
#             cache = get_scrape_cache()
#             lib = cache.link_library
#             user_id = lib.get(placement[1])
#             if user_id != None and user_id != '':
#                 placement[1] = user_id
#
#         return placements
#
# def get_matchplay(soup):
#     placements = []
#     tables = soup.find(id="matchplay-content")
#     if tables is not None:
#         if tables is not None:
#             rows = tables.find_all('tr')
#             if rows is not None:
#                 for row in rows:
#                     if row is not None and row.children is not None:
#                         con = False
#                         for item in row.children:
#                             if item.string is not None and 'Total' in item.string:
#                                 con = True
#                                 break
#                         if con == True:
#                             continue
#
#                         place = None
#                         name = None
#                         score = None
#                         count = 1
#                         for item in row.children:
#                             if count == 5: count = 1
#                             if item is not None and item.string is not None and '\\n' not in item.string and '\n' not in item.string:
#                                 if count == 1:
#                                     place = item.string
#                                     count = count + 1
#                                 elif count == 2:
#                                     name = row.find('a', href=True, text=True)
#                                     name = name['href']
#                                     count = count + 1
#                                 elif count == 3:
#                                     score = item.string
#                                     count = count + 1
#                         placements.append([place, name, score])
#
#     for placement in placements:
#         cache = get_scrape_cache()
#         lib = cache.link_library
#         user_id = lib.get(placement[1])
#         if user_id != None and user_id != '':
#             placement[1] = user_id
#
#     return placements


def get_game_data(tournament, soup):
    table = soup.find(id="qualifying")
    if table:
        rows = table.find_all('tr')
        if rows:
            for row in rows:
                columns = row.find_all('td')
                if columns:
                    title = columns[1]
                    columns = columns[2:-1]
                    if title:
                        tag = title.find('a')
                        if tag:
                            url = tag.get('href')
                            if url and '/bowler/' in url:
                                soup_url = 'https://scratchbowling.com' + url
                                user = User.objects.filter(soup_url=soup_url).first()
                                if user:
                                    game = 1
                                    for score in columns:
                                        tournament.update_game_from_soup(user.id, game, try_int(score.text))
                                        game += 1

def get_oil(soup):
    return None
    title = soup.find(class_='field field--name-field-oil-pattern field--type-entity-reference field--label-inline')
    if title is not None:
        entry = title.find(class_='field__items')
        entry = entry.find(class_='field__item')
        entry = entry.find('a')
        return entry['href']
    return None

def get_image(soup):
    img = soup.find(class_='image-style-tournament-image')
    if img:
        return img.get('src')
    return None



def try_int(value):
    try:
        return int(value)
    except ValueError:
        return 0