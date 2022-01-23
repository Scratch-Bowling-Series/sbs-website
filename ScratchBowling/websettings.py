import json



class WebSettings:
    primary_domain = 'https://www.bowl.sbs'
    os_path = 'C:/Users/Christian J Starr/Documents/ScratchBowlingSeries/Scratch-Bowling-Series-Website/'
    #'/home/scratchbowling/Scratch-Bowling-Series-Website/'


    allow_traffic = True
    allow_signup = True
    allow_login = True
    allow_donations = True
    allow_streaming = True

    maintenance_reason = ''
    maintenance_time = '1 Hour'

    bowler_of_month = None





def store_settings(settings):
    data = [settings.primary_domain,
            settings.os_path,
            settings.allow_traffic,
            settings.allow_signup,
            settings.allow_login,
            settings.allow_donations,
            settings.allow_streaming,
            settings.maintenance_reason,
            settings.maintenance_time,
            settings.bowler_of_month]

    store_file(str(json.dumps(data)))

def get_settings():
    read_file()

def store_file(data, file_name, path=''):
    try:
        settings = WebSettings()
        f = open(settings.os_path + path + file_name, "w")
        f.write(data)
        f.close()
        return True
    except FileNotFoundError:
        return None

def read_file(path, file_name):
    try:
        settings = WebSettings()
        f = open(settings.os_path + path + file_name, "r")
        return f.read()
    except FileNotFoundError:
        return None


