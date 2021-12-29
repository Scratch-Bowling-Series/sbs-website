import json
import os
from itertools import islice
from ScratchBowling.sbs_utils import is_valid_uuid
from accounts.views import User


def Transfer():
    return
    trans = []
    users = User.objects.all()
    length = len(users)
    x = 0
    print('Converting Users to List')
    for user in users:
        x += 1
        print('User (' + str(x) + '/' + str(length) +')')
        usrlist = UserToList(user)
        if usrlist != None:
            trans.append(usrlist)
    export = json.dumps(trans)
    StoreJson(export)


def Gather():
    User.objects.all().delete()

    datas = ReadJson()
    datas = json.loads(datas)
    users = []
    batch_size = 500
    for data in datas:
        user = CreateUserFromList(data)
        if user:
            users.append(user)

    count = 0
    while True:
        count += 1
        start = 0 + (batch_size * (count - 1))
        batch = list(islice(users, start, batch_size * count))
        if not batch:
            break
        User.objects.bulk_create(batch, batch_size)


def UserToList(user):
    usrlist = [
        str(user.id),
        user.first_name,
        user.last_name,
        user.email,
        user.city,
        user.state,
        user.statistics
    ]
    if ValidateUserList(usrlist):
        return usrlist

def CreateUserFromList(data):
    if data != None:
        user = User()
        user.id = is_valid_uuid(data[0])
        user.first_name = data[1]
        user.last_name = data[2]
        user.city = data[4]
        user.state = data[5]
        user.statistics = data[6]
        return user

def ValidateUserList(usrlist):
    if usrlist[1] == None or usrlist[1] == '':
        return False
    if usrlist[2] == None or usrlist[2] == '':
        return False
    if usrlist[4] == None or usrlist[4] == '':
        return False
    if usrlist[5] == None or usrlist[5] == '':
        return False
    return True

def StoreJson(value):
    try:
        pwd = os.path.dirname(__file__)
        f = open(pwd + "/transfer_users.dat", "w")
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
        f = open(pwd + "/transfer_users.dat", "r")
        print('Gathered')
        return f.read()
    except FileNotFoundError:
        return 0
