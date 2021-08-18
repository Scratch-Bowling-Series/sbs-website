import datetime
import json
import os

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
    datas = json.loads(datas)
    for data in datas:
        CreateTournamentFromList(data)

def TournamentToList(tournament):
    tournamentslist = [
        tournament.tournament_name,
        str(tournament.tournament_date),
        tournament.tournament_description,
        str(tournament.tournament_time),
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
        tournament.tournament_name = data[0]
        if data[1] != None:
            tournament.tournament_date = data[1]
        tournament.tournament_description = data[2]
        if data[3] == None or data[3] == 'None':
            data[3] = '12:00'
        tournament.tournament_time = data[3]
        tournament.center = data[4]
        tournament.entry_fee = data[5]
        tournament.qualifiers = data[6]
        tournament.matchplay = data[7]
        tournament.format = data[8]
        tournament.save()

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
