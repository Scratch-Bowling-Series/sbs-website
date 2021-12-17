import datetime
import json
import os
from itertools import islice

from tournaments.models import Tournament


def TransferT():
    trans = []
    tournaments = Tournament.objects.all()
    length = len(tournaments)
    x = 0
    print('Converting Tournaments to List')
    for tournament in tournaments:
        x += 1
        print('User (' + str(x) + '/' + str(length) +')')
        tournamentslist = TournamentToList(tournament)
        if tournamentslist != None:
            trans.append(tournamentslist)
    export = json.dumps(trans)
    StoreJson(export)

def Gather():
    Tournament.objects.all().delete()
    datas = ReadJson()
    if datas == None:
        return
    datas = json.loads(datas)
    batch_size = 200
    count = 0
    while True:
        tournaments = []
        count += 1
        start = 0 + (batch_size * (count - 1))
        data_batch = list(islice(datas, start, batch_size * count))
        if not data_batch:
            break
        for data in data_batch:
            tournaments.append(CreateTournamentFromList(data))
        Tournament.objects.bulk_create(tournaments, batch_size)





def TournamentToList(tournament):
    tournamentslist = [
        tournament.name,
        tournament.datetime,
        tournament.description,
        tournament.center,
        tournament.entry_fee,
        tournament.qualifiers,
        tournament.matchplay,
        tournament.format
    ]
    if ValidateTournamentList(tournamentslist):
        return tournamentslist

def CreateTournamentFromList(data):
    if data != None:
        tournament = Tournament()
        tournament.name = data[0]
        if data[1] != None:
            tournament.tournament_date = data[1]
        tournament.description = data[2]
        if data[3] == None or data[3] == 'None':
            data[3] = '12:00'
        tournament.tournament_time = data[3]
        tournament.center = data[4]
        tournament.entry_fee = data[5]
        tournament.qualifiers = data[6]
        tournament.matchplay = data[7]
        tournament.format = data[8]
        return tournament

def ValidateTournamentList(usrlist):
    if usrlist[0] == None or usrlist[0] == '':
        return False
    return True

def StoreJson(value):
    try:
        pwd = os.path.dirname(__file__)
        f = open(pwd + "/transfer_tournaments.dat", "w")
        f.write(str(value))
        f.seek(0, os.SEEK_END)
        size = f.tell()
        print('Data Stored! File Size: ' + str(size) + 'bytes')
        f.close()
    except FileNotFoundError:
        return 0

def ReadJson():
    try:
        pwd = os.path.dirname(__file__)
        f = open(pwd + "/transfer_tournaments.dat", "r")
        print('Gathered')
        return f.read()
    except FileNotFoundError:
        return 0
