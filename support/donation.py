import os


def set_count(value):
    try:
        pwd = os.path.dirname(__file__)
        f = open(pwd + "/donation-count.dat", "w")
        f.write(str(value))
        print('ran')
        f.close()
    except FileNotFoundError:
        return 0

def get_donation_count():
    try:
        pwd = os.path.dirname(__file__)
        f = open(pwd + "/donation-count.dat", "r")
        return int(f.read())
    except FileNotFoundError:
        return 0
