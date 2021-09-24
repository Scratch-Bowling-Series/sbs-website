from ScratchBowling.sbs_utils import is_valid_uuid


def add_user_to_roster_obj(tournament, user_id):
    roster_data = tournament.roster
    if roster_data != None:
        user_id = is_valid_uuid(user_id)
        if user_id != None:
            user_id = str(user_id)
            roster = quickle.loads(roster_data)
            roster_length = len(roster)
            if roster_length < tournament.spots_reserved:
                exists = False
                for user in roster:
                    if user == user_id:
                        exists = True
                if not exists:
                    roster.append(user_id)
                    tournament.roster = quickle.dumps(roster)


def remove_user_from_roster_obj(tournament, user_id):
    roster_data = tournament.roster
    if roster_data != None:
        user_id = is_valid_uuid(user_id)
        if user_id != None:
            user_id = str(user_id)
            roster = quickle.loads(roster_data)
            new_roster = []
            for user in roster:
                if user != user_id:
                    new_roster.append(user)
            tournament.roster = quickle.dumps(new_roster)


def get_roster_length_obj(tournament):
    roster_data = tournament.roster
    if roster_data != None:
        roster = quickle.loads(roster_data)
        if roster != None:
            return len(roster)


def get_spots_available_obj(tournament):
    roster_data = tournament.roster
    if roster_data != None:
        roster = quickle.loads(roster_data)
        if roster != None:
            available = tournament.spots_reserved - len(roster)
            if available < 0:
                available = 0
            return available


def serialize_roster_data(roster):
    return quickle.dumps(roster)


def deserialize_roster_data(roster_data):
    return quickle.loads(roster_data)