import json
import time
import uuid
from datetime import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from accounts.forms import User
from tournaments.models import Tournament


class ScrapedTournament:
    name = ''
    n_city = ''
    date = None
    center = None
    entry = 0
    qualifiers = None
    oil = None
    matchplay = None


us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
    'Ontario': 'ON'
}

def convert_tournaments(jsonstr):
    Tournament.objects.all().delete()
    datas = json.loads(jsonstr)
    length = len(datas)
    count = 0
    for data in datas:
        name = data[0]
        count = count + 1
        if data is not None and data[1] != 'None' and data[1] is not None:
            tournament = Tournament.create(name)
            date = datetime.strptime(data[1], '%m/%d/%y')
            tournament.tournament_date = date.strftime('%Y-%m-%d')
            tournament.tournament_oil = data[2]
            tournament.tournament_center = data[3]
            tournament.entry = data[4]
            tournament.qualifiers = json.dumps(data[5])
            tournament.matchplay = json.dumps(data[6])
            print('Adding Tournament (' + str(count) + '/' + str(length) + ')')
            tournament.save()
    return assign_players()


def scrape_tournaments_task():
    urls = get_page_urls()
    tournaments = []
    amount = 0
    total = 0
    waittime = 0
    for url in urls:
        waittime = waittime + 1
        start_time = time.time()
        amount = amount + 1
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
            if date is not None and skip is False:
                tournament.date = date
            else:
                skip = True

            center = get_center(soup)
            if center is not None and skip is False:
                tournament.center = center
            else:
                skip = True

            entry = get_entry(soup)
            if entry is not None and skip is False:
                tournament.entry = entry
            else:
                skip = True

            qualifiers = get_qualifiers(soup)
            if qualifiers is not None and skip is False:
                tournament.qualifiers = qualifiers
            else:
                skip = True

            matchplay = get_matchplay(soup)
            if matchplay is not None and skip is False:
                tournament.matchplay = matchplay
            else:
                skip = True

            oil = get_oil(soup)
            if oil is not None and skip is False:
                tournament.oil = oil
            else:
                skip = False

            if skip is False:
                tournaments.append(tournament)

            second = time.time() - start_time
            total = total + second
            second = total / amount
            second = (second * (len(urls) - amount)) / 60
            second = ') (%.2f' % second
            print('Scraping...  (' + str(amount) + '/' + str(len(urls)) + second + 'M Remain)')

            if waittime == 200:
                time.sleep(10)

    return convert_tournaments(easy_display(tournaments))


def easy_display(tournaments):
    info = []
    for tournament in tournaments:
        name = tournament.name
        date = tournament.date
        center = tournament.center
        oil = tournament.oil
        entry = tournament.entry
        qualifiers = tournament.qualifiers
        matchplay = tournament.matchplay

        data = [name, date, oil, center, entry, qualifiers, matchplay]
        info.append(data)
    return json.dumps(info)


def get_page_urls():
    urls = []
    tries = 0

    for x in range(0, 34):
        with urlopen('https://www.scratchbowling.com/tournament-results?page=' + str(x)) as response:
            soup = BeautifulSoup(response, 'lxml')
            titles = soup.find_all(class_='field field--name-title field--type-string field--label-hidden')
            if len(titles) == 0:
                tries + 1
                if tries > 4:
                    return urls
            for title in titles:
                url = title.find_parent('a').get('href')
                if 'oil-patterns' not in url:
                    urls.append('https://scratchbowling.com/' + url)

    print('Finished Loading URLS')
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
                        data = (place, name, score)
                        placements.append(data)

    return placements


def get_oil(soup):
    title = soup.find(class_='field field--name-field-oil-pattern field--type-entity-reference field--label-inline')
    if title is not None:
        entry = title.find(class_='field__items')
        entry = entry.find(class_='field__item')
        entry = entry.find('a')
        return entry['href']

    return None


User = get_user_model()


def create_accounts_from_json():
    file = open('bowlers.txt', 'r')
    jsonstr = file.read()
    bowlersdata = json.loads(jsonstr)

    output = ''
    for bowler in bowlersdata:
        first_name = output + bowler[0].split(' ', 1)[0]
        last_name = ''
        city = ''
        state = ''

        if len(bowler[0].split(' ', 1)) > 1:
            last_name = bowler[0].split(' ', 1)[1]

        if len(bowler[1].split(',')) > 1:
            city = bowler[1].split(',')[0]

        if len(bowler[1].split(',')) > 1:
            state = bowler[1].split(',')[1]
            state = convert_abr(state)
        tempemail = first_name + last_name + city + '@temp.com'
        if User.objects.filter(email=tempemail).count() == 0:
            user = User.objects.create_user(tempemail, 'temp')
            user.first_name = first_name
            user.last_name = last_name
            user.location_state = state
            user.location_city = city
            user.save()
            print('ADDED ' + first_name)
        else:
            print('SKIPPED ' + first_name)

    return output


def convert_abr(state):
    state_rev = dict(map(reversed, us_state_abbrev.items()))
    state = state.replace(' ', '')
    state = state.upper()

    if state in state_rev:
        return state_rev[state]
    else:
        return state


def scrape_bowlers():
    urls = get_account_urls(34)
    bowlers = []
    count = 0
    waittime = 0
    length = len(urls)
    average = 0;
    started_time = time.time()
    for url in urls:
        count = count + 1
        waittime = waittime + 1
        if waittime == 500:
            waittime = 0
            time.sleep(20)
        start_time = time.time()
        with urlopen(url) as response:
            soup = BeautifulSoup(response, 'lxml')
            bowler_name = soup.find(class_="field field--name-title field--type-string field--label-hidden").text
            location = soup.find(class_="col-sm-3")
            location = location.find(class_='field__item').text
            bowlers.append([bowler_name, location])

            second = time.time() - start_time
            average = average + second
            second = average / count
            second = (second * (length - count)) / 60
            second = ') (%.2f' % second
            print('Getting Bowler Data: (' + str(count) + '/' + str(length) + second + ' Minutes Remain)')

    times = " (%.2F)" % ((time.time() - started_time) / 60)
    print(str(count) + ' DONE: Time Taken:' + times)

    return json.dumps(bowlers)


def get_account_urls(pages):
    urls = []
    for x in range(0, pages):
        with urlopen('http://www.scratchbowling.com/bowler-bios?page=' + str(x)) as response:
            print('Scraping Bowler Page: (' + str(x) + '/' + str(pages) + ')')
            soup = BeautifulSoup(response, 'lxml')
            titles = soup.find_all(class_='views-field views-field-title')
            if titles is not None:
                for title in titles:
                    title = title.find('a')
                    if title is not None:
                        urls.append('http://www.scratchbowling.com' + title.get('href'))
    print('Fetched Urls. Amount: ' + str(len(urls)))
    return urls


user_library = {}


def assign_players():
    load_library()
    tournaments = Tournament.objects.all()
    length = len(tournaments)
    count = 0


    for tournament in tournaments:
        count = count + 1
        qualstring = tournament.qualifiers.replace("'", '"')
        try:
            qualifiers = json.loads(qualstring)
        except ValueError:
            continue
        matchstring = tournament.matchplay.replace("'", '"').replace('(', '[').replace(')', ']')
        try:
            matchplay = json.loads(matchstring)
        except ValueError:
            continue
        if qualifiers is None or matchplay is None:
            continue
        for qual in qualifiers:

            temp = check_player(qual[1])
            if temp is not None:
                qual[1] = temp

        tournament.qualifiers = json.dumps(qualifiers)
        tournament.save()

        for match in matchplay:
                temp = check_player(match[1])
                if temp is not None:
                    match[1] = temp

        tournament.matchplay = json.dumps(matchplay)
        tournament.save()

        print('SUCCESS (' + str(count) + '/' + str(length) + ')')

        save_library()


def save_library():
    file = open('library.txt', 'w')
    file.write(json.dumps(user_library))
    file.close()


def load_library():
    file = open('library.txt', 'r')
    data = file.read()
    if data is not None and len(data) > 0:
        global user_library
        user_library = json.loads(data)


def check_player(url):
    if '/bowler/' in url:
        if url in user_library:
            data = user_library[url]
            return data
        else:
            temp = get_uuid(url)
            if temp is not None:
                temp = str(temp.user_id)
                user_library[url] = temp
                return temp
    return None


def get_uuid(url):
    with urlopen('https://scratchbowling.com' + url) as response:
        soup = BeautifulSoup(response, 'lxml')
        bowler_name = soup.find(class_="field field--name-title field--type-string field--label-hidden").text
        first_name = bowler_name.split(' ', 1)[0]
        last_name = bowler_name.split(' ', 1)[1]
        location = soup.find(class_="col-sm-3")
        location = location.find(class_='field__item').text
        city = ''
        state = ''
        if len(location.split(',')) > 1:
            city = location.split(',')[0]

        if len(location.split(',')) > 1:
            state = location.split(',')[1]
            state = convert_abr(state)

        users = User.objects.filter(first_name=first_name, last_name=last_name)
        if len(users) > 1:
            users = users.filter(location_city=city)
            if len(users) > 1:
                users = users.get(location_state=state)
                if len(users) > 1:
                    return None
                elif users is not None and len(users) == 1:
                    return users[0]
            elif users is not None and len(users) == 1:
                return users[0]
        elif users is not None and len(users) == 1:
            return users[0]


def is_valid_uuid(val):
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None






