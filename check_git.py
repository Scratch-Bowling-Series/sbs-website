




def get_last_commit():
    file = open('/.git/COMMIT_EDITMSG', 'r')
    print(file.read())