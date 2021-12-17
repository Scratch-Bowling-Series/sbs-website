import uuid

from ScratchBowling.websettings import WebSettings


def is_valid_uuid(val):
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None

def make_ordinal(n):
    n = int(n)
    if n == 0:
        return '0'
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix


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

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
    'Ontario': 'ON'
}

def normalize_state(state, abbrev=False):
    if state == None:
        return ''
    if state[0] == ' ':
        state = state[1:]
    if len(state) > 2 and state[len(state) - 1] == ' ':
        state = state[:len(state) - 1]

    if len(state) == 2:
        state_rev = dict(map(reversed, us_state_abbrev.items()))
        state = state.replace(' ', '')
        state = state.replace(',', '')
        state = state.upper()
        state_abbrev = state_rev.get(state)
        if state_abbrev != None:
            if abbrev:
                return state
            else:
                return state_abbrev
    if len(state) > 2:
        state = state.title()
        state = state.replace(',', '')
        state_abbrev = us_state_abbrev.get(state)
        if state_abbrev != None:
            if abbrev:
                return state_abbrev
            else:
                return state
    return state