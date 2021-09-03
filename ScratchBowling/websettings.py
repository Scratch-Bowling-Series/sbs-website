import json

from ScratchBowling.sbs_utils import read_file, store_file


class WebSettings:
    primary_domain = 'https://scratchbowling.com'
    os_path = '/home/scratchbowling/Scratch-Bowling-Series-Website/'


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



