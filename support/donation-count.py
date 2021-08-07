
def set_count(value):
    f = open("donation-count.dat", "w")
    f.write(str(value))
    print('ran')
    f.close()

def get_count():
    f = open("donation-count.dat", "r")
    return int(f.read())