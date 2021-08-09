




def get_last_commit():
    file = open('/home/scratchbowling/Scratch-Bowling-Series-Website/.git/COMMIT_EDITMSG', 'r')
    print(file.read())