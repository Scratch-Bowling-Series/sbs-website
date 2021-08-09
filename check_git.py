import datetime


def get_last_commit():
    file = open('/home/scratchbowling/Scratch-Bowling-Series-Website/.git/COMMIT_EDITMSG', 'r')
    return file.read()

def main():
    file = open('/home/scratchbowling/Scratch-Bowling-Series-Website/.git/COMMIT_EDITMSG', 'w')
    file.write(str(datetime.datetime.now()))



if __name__ == "__main__":
    main()