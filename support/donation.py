import os


def set_count(value):
    pwd = os.path.dirname(__file__)
    f = open(pwd + "/donation-count.dat", "w")
    f.write(str(value))
    print('ran')
    f.close()

def get_donation_count():
    pwd = os.path.dirname(__file__)
    f = open(pwd + "/donation-count.dat", "r")
    return int(f.read())