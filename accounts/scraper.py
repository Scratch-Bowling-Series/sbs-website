import json
import time
from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model

from tournaments.tournament_scraper import convert_abr

User = get_user_model()

def UpdateUsers():
    urls = get_account_urls(5)
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

    bowlers_added = 0
    bowlers_skipped = 0
    total_bowlers = 0
    for bowler in bowlers:
        total_bowlers += 1
        first_name = bowler[0].split(' ', 1)[0]
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
            bowlers_added += 1
        else:
            bowlers_skipped += 1
    return 'Bowlers Added: ' + str(bowlers_added) + '<br><br>' + 'Bowlers Skipped: ' + str(bowlers_skipped) + '<br><br>' + 'Total Bowlers: ' + str(total_bowlers)


def get_account_urls(pages):
    urls = []
    for x in range(35 - pages, 35):
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









