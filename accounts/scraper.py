import json
import time
from itertools import islice
from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model

from tournaments.tournament_scraper import convert_abr

User = get_user_model()

def UpdateUsers():
    urls = get_account_urls(5)
    users = []
    bowlers_added = 0
    for url in urls:
        user = get_user_from_url(url)
        if user:
            bowlers_added += 1
            users.append(user)

    batch_size = 500
    count = 0
    while True:
        count += 1
        start = 0 + (batch_size * (count - 1))
        batch = list(islice(users, start, batch_size * count))
        if not batch:
            break
        User.objects.bulk_create(batch, batch_size)



    return 'Bowlers Added: ' + str(bowlers_added)


def get_account_urls(pages):
    urls = []
    for x in range(38 - pages, 38):
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


def get_user_from_url(url):
    with urlopen(url) as response:
        soup = BeautifulSoup(response, 'lxml')
        bowler_name = soup.find(class_="field field--name-title field--type-string field--label-hidden").text
        location = soup.find(class_="col-sm-3")
        location = location.find(class_='field__item').text
        if bowler_name == None or location == None or len(bowler_name) > 0 or len(location) > 0:
            return None

        first_name = bowler_name.split(' ', 1)[0]
        last_name = ''
        city = ''
        state = ''
        if len(bowler_name.split(' ', 1)) > 1:
            last_name = bowler_name.split(' ', 1)[1]
        if len(location.split(',')) > 1:
            city = location.split(',')[0]
        if len(bowler_name.split(',')) > 1:
            state = location.split(',')[1]
            state = convert_abr(state)

        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.location_state = state
        user.location_city = city








