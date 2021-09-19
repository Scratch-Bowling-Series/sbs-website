import json
from datetime import datetime
import quickle
import os
import time
import uuid
from itertools import islice
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from ScratchBowling.sbs_utils import is_valid_uuid, normalize_state
from centers.models import Center
from scoreboard.ranking import calculate_statistics
from tournaments.models import Tournament
from tournaments.tournament_data import convert_to_tournament_data_all_tournaments


User = get_user_model()

## SCRAPE CACHE ##
class ScrapeCache(quickle.Struct):
    last_scrape : str = None
    link_library : dict = {}
    center_link_library : dict = {}
    tournament_link_library : dict = {}
    urls : list = []

def store_scrape_cache(scrape_cache):
    try:
        pwd = os.path.dirname(__file__)
        f = open(pwd + "/scrape_cache.dat", "wb")
        f.write(serialize_scrape_cache(scrape_cache))
        f.close()
    except FileNotFoundError:
        return None

def convert_to_new_scrape_cache():
    scrape_cache = get_old_scrape_cache()
    store_scrape_cache(scrape_cache)
    print('DONE')

def get_old_scrape_cache():
    try:
        pwd = os.path.dirname(__file__)
        f = open(pwd + "/scrape_cache.dat", "r")
        data = f.read()
        if data != None and len(data) > 0:
            data = json.loads(data)
            if data != None:
                cache = ScrapeCache()
                cache.last_scrape = data[0]
                cache.urls = data[1]
                cache.link_library = data[2]
                cache.center_link_library = data[3]
                cache.tournament_link_library = data[4]
                return cache
        return ScrapeCache()
    except FileNotFoundError:
        return ScrapeCache()

def get_scrape_cache():
    try:
        pwd = os.path.dirname(__file__)
        f = open(pwd + "/scrape_cache.dat", "rb")
        return deserialize_scrape_cache(f.read())
    except FileNotFoundError:
        return ScrapeCache()

def serialize_scrape_cache(scrape_cache):
    return quickle.Encoder(registry=[ScrapeCache]).dumps(scrape_cache)

def deserialize_scrape_cache(data):
    return quickle.Decoder(registry=[ScrapeCache]).loads(data)

## MASTER SCRAPE FUNCTION ##
def master_scrape(update=True, debug=False):
    logit('Startup Initialized - Update: ' + str(update) + ' - Debug: ' + str(debug))
    ## SCRAPE FOR NEW USERS ##
    if update == False: User.objects.all().delete()
    users_added = scrape_for_new_users(update, debug)
    logit('Users Accounts Scrape', 'Complete - Added: ' + str(users_added))

    ## SCRAPE FOR NEW CENTERS ##
    if update == False: Center.objects.all().delete()
    centers_added = scrape_for_new_centers(update, debug)
    logit('Bowling Centers Scrape', 'Complete - Added: ' + str(centers_added))

    ## SCRAPE FOR NEW TOURNAMENTS ##
    if update == False: Tournament.objects.all().delete()
    tournaments_added = scrape_for_new_tournaments(update, debug)
    logit('Tournaments Scrape', 'Complete - Added: ' + str(tournaments_added))

    ## CONVERT SCRAPE DATA TO TOURNAMENT DATA
    convert_to_tournament_data_all_tournaments()
    logit('Converting Tournaments', 'Complete - Converted: ' + str(tournaments_added))
    ## CALCULATE NEW STATISTICS
    calculate_statistics()
    logit('Calculating Statistics', 'Complete - Calculated: ' + str(users_added))
    ## UPDATE CACHE DATE ##
    cache = get_scrape_cache()
    if cache != None:
        cache.last_scrape = str(datetime.now())
        store_scrape_cache(cache)

    logit('Finished')


## USER ACCOUNT SCRAPING ##
def scrape_for_new_users(update, debug):
    urls = get_all_account_urls()
    cache = get_scrape_cache()
    lib = cache.link_library
    bowlers_added = 0
    step = 0
    amount = 0
    elapsed_total = 0
    elapsed_count = 0
    last_minutes_remaining = 0
    if debug: urls = urls[:200]
    urls_length = len(urls)
    batch_size = 200
    count = 0
    while True:
        users = []
        count += 1
        start = 0 + (batch_size * (count - 1))
        url_batch = list(islice(urls, start, batch_size * count))
        if not url_batch:
            break
        for url in url_batch:
            start = time.time()
            step += 1
            user = get_user_from_url(url)
            if user != None:
                if update:
                    search = User.objects.filter(first_name=user.first_name, last_name=user.last_name,
                                                 location_city=user.location_city,
                                                 location_state=user.location_state).first()
                    if search == None:
                        bowlers_added += 1
                        users.append(user)
                        if user.user_id != None:
                            lib[url] = str(user.user_id)
                        else:
                            user.user_id = uuid.uuid4
                            lib[url] = str(user.user_id)
                    else:
                        lib[url] = str(search.user_id)
                else:
                    bowlers_added += 1
                    users.append(user)
                    if user.user_id != None:
                        lib[url] = str(user.user_id)
                    else:
                        user.user_id = uuid.uuid4
                        lib[url] = str(user.user_id)
            end = time.time()
            elapsed = end - start
            elapsed_total += elapsed
            elapsed_count += 1
            if step == 10:
                amount += 10
                step = 0
                minutes_remaining = int(((elapsed_total / elapsed_count) * (urls_length - amount)) / 60)
                if last_minutes_remaining != minutes_remaining:
                    last_minutes_remaining = minutes_remaining
                    logit('Users Accounts Scrape',
                          str(int((amount / urls_length) * 100)) + '% - Time Remaining: ' + str(
                              minutes_remaining) + ' Minutes - Elapsed: ' + str(int(elapsed_total / 60)) + ' Minutes')
        User.objects.bulk_create(users, batch_size)
    cache.link_library = lib
    store_scrape_cache(cache)
    return bowlers_added

def get_all_account_urls():
    page = 0
    all_urls = []
    while True:
        page += 1
        logit('Users Accounts Gather Urls', str(int((page / 35) * 100)) + '%')
        cache = get_scrape_cache()
        lib = cache.link_library
        urls = get_account_urls(page)
        if urls == None or len(urls) == 0:
            break
        for url in urls:
            url = str(url)
            all_urls.append(url)
            if lib.get(url) == None:
                lib[url] = 'empty'
        cache.link_library = lib
        store_scrape_cache(cache)
    return all_urls

def get_account_urls(page):
    urls = []
    with urlopen('http://www.scratchbowling.com/bowler-bios?page=' + str(page)) as response:
        soup = BeautifulSoup(response, 'lxml')
        titles = soup.find_all(class_='views-field views-field-title')
        if titles is not None:
            for title in titles:
                title = title.find('a')
                if title is not None:
                    urls.append(title.get('href'))
    return urls

def get_user_from_url(url):
    url = 'http://www.scratchbowling.com' + url
    with urlopen(url) as response:
        soup = BeautifulSoup(response, 'lxml')
        bowler_name = soup.find(class_="field field--name-title field--type-string field--label-hidden").text
        location = soup.find(class_="col-sm-3")
        location = location.find(class_='field__item').text
        if bowler_name == None or location == None or len(bowler_name) == 0 or len(location) == 0:
            return None
        user = User()
        user.first_name = bowler_name.split(' ', 1)[0]
        if len(bowler_name.split(' ', 1)) > 1:
            user.last_name = bowler_name.split(' ', 1)[1]
        if len(location.split(',')) > 1:
            user.location_city = location.split(',')[0]
            user.location_state = normalize_state(location.split(',')[1])
        user.unclaimed = True
        return user


## CENTERS SCRAPING ##
def scrape_for_new_centers(update, debug):
    cache = get_scrape_cache()
    lib = cache.center_link_library
    centers = []
    urls = get_all_center_urls()
    if debug: urls = urls[:100]
    urls_length = len(urls)
    amount = 0
    step = 0
    logit('Bowling Centers Scrape', '0%')
    for url in urls:
        step += 1
        if step == 100:
            amount += 100
            step = 0
            logit('Bowling Centers Scrape', str(int((amount / urls_length) * 100)) + '%')
        center = get_center_from_url(url)
        if center != None:
            if update:
                if center_exists(center) == False:
                    centers.append(center)
                    if center.center_id != None:
                        lib[url] = str(center.center_id)
                else:
                    lib[url] = str(center.center_id)
            else:
                centers.append(center)
                if center.center_id != None:
                    lib[url] = str(center.center_id)

    cache.center_link_library = lib
    store_scrape_cache(cache)
    batch_size = 100
    count = 0
    centers_added = len(centers)
    while True:
        count += 1
        start = 0 + (batch_size * (count - 1))
        batch = list(islice(centers, start, batch_size * count))
        if not batch:
            break
        Center.objects.bulk_create(batch, batch_size)
    return centers_added

def get_all_center_urls():
    page = 0
    urls = []
    while True:
        page += 1
        logit('Bowling Centers Gather Urls', str(int((page / 5) * 100)) + '%')
        with urlopen('https://www.scratchbowling.com/bowling-centers?page=' + str(page)) as response:
            soup = BeautifulSoup(response, 'lxml')
            rows = soup.find_all(class_="views-row")
            if rows == None or len(rows) == 0:
                break
            for row in rows:
                title = row.find(class_="node__title")
                if title != None:
                    url = title.find('a')
                    url = url.get('href')
                    if url != None:
                        urls.append(str(url))
    return urls

def center_exists(center):
    center = Center.objects.filter(center_name=center.center_name, location_city=center.location_city).first()
    if center != None:
        return True
    else:
        return False

def get_center_from_url(url):
    with urlopen('http://www.scratchbowling.com' + url) as response:
        soup = BeautifulSoup(response, 'lxml')

        name = soup.find(class_='title')
        if name != None:
            name = name.find('span')
            if name != None:
                name = name.text

        address = soup.find(class_='address')
        if address != None:
            street = address.find(class_='address-line1')
            if street != None:
                street = street.text
            city = address.find(class_='locality')
            if city != None:
                city = city.text
            state = address.find(class_='administrative-area')
            if state != None:
                state = state.text
            zip = address.find(class_='postal-code')
            if zip != None:
                zip = zip.text
                if zip != None:
                    zip = int(zip)

        phone = soup.find(class_="field--name-field-phone-number")
        if phone != None:
            phone = phone.find("a")
            if phone != None:
                phone = phone.text
                phone = phone.replace('(', '')
                phone = phone.replace(')', '')
                phone = phone.replace('-', '')
                phone = phone.replace(' ', '')

        description = soup.find(class_="field--name-field-website")
        if description != None:
            description = description.find("a")
            if description != None:
                description = description.text

    return create_center(name, street, city, state, zip, phone, description)

def create_center(name, street, city, state, zip, phone, description):
    center = Center()
    center.center_name = name
    center.location_street = street
    center.location_city = city
    center.location_state = state
    center.location_zip = zip
    if phone is None:
        phone = 0
    center.phone_number = int(phone)
    center.center_description = str(description) + ' '
    return center

## TOURNAMENT SCRAPING ##
class ScrapedTournament:
    name = ''
    n_city = ''
    date = None
    center = None
    entry = 0
    qualifiers = None
    oil = None
    matchplay = None

def scrape_for_new_tournaments(update, debug):
    urls = get_page_urls()
    count = 0
    tournaments_added = 0
    tournaments = []
    step = 0
    amount = 0
    if debug: urls = urls[:50]
    urls_length = len(urls)
    logit('Tournaments Scrape', '0%')
    for url in urls:
        count += 1
        step += 1
        if step == 25:
            amount += 25
            step = 0
            logit('Tournaments Scrape', str(int((amount / urls_length) * 100)) + '%')
        tournament = get_tournament_from_url(url)
        if tournament != None:
            if update:
                if tournament_exists(tournament) == False:
                    tournaments.append(tournament)
                    tournaments_added += 1
            else:
                tournaments.append(tournament)
                tournaments_added += 1
        if count == 200:
            time.sleep(10)
    tournaments = convert_tournaments(tournaments)
    if len(tournaments) == 0:
        return 0
    batch_size = 100
    count = 0
    while True:
        count += 1
        start = 0 + (batch_size * (count - 1))
        batch = list(islice(tournaments, start, batch_size * count))
        if not batch:
            break
        Tournament.objects.bulk_create(batch, batch_size)
    return tournaments_added

def tournament_exists(scraped_tournament):
    if scraped_tournament != None:
        tournament = Tournament.objects.filter(tournament_name=scraped_tournament.name, tournament_date=scraped_tournament.date).first()
        if tournament == None:
            return False
        else:
            return True
    return False

def convert_tournaments(datas):
    tournaments = []
    cache = get_scrape_cache()
    lib = cache.center_link_library
    for data in datas:
        tournament = Tournament.create(data.name)
        if data.date == None: data.date = '01/01/01'
        date = datetime.strptime(data.date, '%m/%d/%y')
        tournament.tournament_date = date.strftime('%Y-%m-%d')
        tournament.tournament_oil = data.oil
        if data.center != None:
            center_id = is_valid_uuid(lib.get(data.center))
            if center_id != None:
                tournament.tournament_center = center_id
        tournament.entry = data.entry
        tournament.qualifiers = json.dumps(data.qualifiers)
        tournament.matchplay = json.dumps(data.matchplay)
        tournaments.append(tournament)
    return tournaments

def get_tournament_from_url(url):
    with urlopen(url) as response:
        soup = BeautifulSoup(response, 'lxml')

        tournament = ScrapedTournament()
        skip = False
        name = get_name(soup)
        if name is not None:
            tournament.name = name
        else:
            skip = True

        date = get_date(soup)
        if date != None and skip == False:
            tournament.date = date
        else:
            skip = True

        center = get_center(soup)
        if center != None and skip == False:
            tournament.center = center
        else:
            skip = True

        entry = get_entry(soup)
        if entry != None and skip == False:
            tournament.entry = entry
        else:
            skip = True

        qualifiers = get_qualifiers(soup)
        if qualifiers != None and skip == False:
            tournament.qualifiers = qualifiers
        else:
            skip = True

        matchplay = get_matchplay(soup)
        if matchplay != None and skip == False:
            tournament.matchplay = matchplay
        else:
            skip = True

        oil = get_oil(soup)
        if oil != None and skip == False:
            tournament.oil = oil
        else:
            skip = False

        if skip == False:
            return tournament
        else:
            return None

def get_page_urls():
    urls = []
    page = 0
    while True:
        page += 1
        logit('Tournaments Gather Urls', str(int((page / 40) * 100)) + '%')
        with urlopen('https://www.scratchbowling.com/tournament-results?page=' + str(page)) as response:
            soup = BeautifulSoup(response, 'lxml')
            titles = soup.find_all(class_='field field--name-title field--type-string field--label-hidden')
            if titles == None or len(titles) == 0:
                break
            for title in titles:
                url = title.find_parent('a').get('href')
                if 'oil-patterns' not in url:
                    urls.append('https://scratchbowling.com/' + url)
    return urls

def get_entry(soup):
    title = soup.find(class_='field field--name-field-entry-fee field--type-string field--label-inline')
    if title is not None:
        entry = title.find(class_='field__item')
        if entry is not None:
            entry = entry.text
            entry = entry.replace("$","")
            if '/' in entry:
                entry = entry.split('/')
                entry = entry[0]
            return entry

    return None

def get_name(soup):
    title = soup.find(class_='field field--name-title field--type-string field--label-hidden')
    if title is not None:
        if '-' in title.text:
            return title.text.split('-')[1]
        else:
            return title.text
    return None

def get_date(soup):
    title = soup.find(class_='field field--name-title field--type-string field--label-hidden')
    if title is not None:
        try:
            date = datetime.strptime(title.text.split('-')[0], '%B %d, %Y ')
            return date.strftime('%m/%d/%y')
        except ValueError:
            date = None
    return None

def get_center(soup):
    title = soup.find(class_='field field--name-field-bowling-center field--type-entity-reference field--label-inline')
    if title is not None:
        entry = title.find(class_='field__items')
        entry = entry.find(class_='field__item')
        entry = entry.find('a')
        return entry['href']

    return None

def get_qualifiers(soup):
    tables = soup.find(id="qualifying-1")
    if tables is not None:
        placements = []
        if tables is not None:
            rows = tables.find_all('tr')
            if rows is not None:
                first = 0
                for row in rows:
                    first = first + 1
                    if first != 1:
                        if row is not None:
                            if row.children is not None:
                                count = 0
                                data = []
                                for item in row.children:
                                    count = count + 1
                                    if count == 4:
                                        name = row.find('a', href=True, text=True)
                                        if name is not None and name['href'] is not None:
                                            data.append(name['href'])
                                    elif item.string != '\n':
                                        data.append(item.string)
                                placements.append(data)

        for placement in placements:
            cache = get_scrape_cache()
            lib = cache.link_library
            user_id = lib.get(placement[1])
            if user_id != None and user_id != '':
                placement[1] = user_id

        return placements

def get_matchplay(soup):
    placements = []
    tables = soup.find(id="matchplay-content")
    if tables is not None:
        if tables is not None:
            rows = tables.find_all('tr')
            if rows is not None:
                for row in rows:
                    if row is not None and row.children is not None:
                        con = False
                        for item in row.children:
                            if item.string is not None and 'Total' in item.string:
                                con = True
                                break
                        if con == True:
                            continue

                        place = None
                        name = None
                        score = None
                        count = 1
                        for item in row.children:
                            if count == 5: count = 1
                            if item is not None and item.string is not None and '\\n' not in item.string and '\n' not in item.string:
                                if count == 1:
                                    place = item.string
                                    count = count + 1
                                elif count == 2:
                                    name = row.find('a', href=True, text=True)
                                    name = name['href']
                                    count = count + 1
                                elif count == 3:
                                    score = item.string
                                    count = count + 1
                        placements.append([place, name, score])

    for placement in placements:
        cache = get_scrape_cache()
        lib = cache.link_library
        user_id = lib.get(placement[1])
        if user_id != None and user_id != '':
            placement[1] = user_id

    return placements

def get_oil(soup):
    title = soup.find(class_='field field--name-field-oil-pattern field--type-entity-reference field--label-inline')
    if title is not None:
        entry = title.find(class_='field__items')
        entry = entry.find(class_='field__item')
        entry = entry.find('a')
        return entry['href']

    return None


## LOGGING ##
def logit(task, prog=None):
    if prog != None:
        print('MasterScraper - Task: ' + str(task) + ' - Progress: ' + str(prog))
        set_scraper_log('MasterScraper - Task: ' + str(task) + ' - Progress: ' + str(prog))
    else:
        print('MasterScraper - Task: ' + str(task))
        set_scraper_log('MasterScraper - Task: ' + str(task))

def set_scraper_log(log):
    try:
        pwd = os.path.dirname(__file__)
        f = open(pwd + "/scrape_log.txt", "a")
        f.write(str(datetime.now()) + ' - ' +  str(log) + '\n')
        f.close()
    except FileNotFoundError:
        return None

def get_scraper_log():
    try:
        pwd = os.path.dirname(__file__)
        f = open(pwd + "/scrape_log.txt", "r")
        logs = f.readlines()
        return logs
    except FileNotFoundError:
        return ScrapeCache()

if __name__ == "__main__":
    master_scrape(False, True)