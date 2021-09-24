import quickle
from django.template.defaulttags import register


## FRIENDS LIST FORMAT : LIST OF UUIDS


# FILTERS
@register.filter
def is_friends_filter(user_id, friends_list):
    return is_friends_with(friends_list, user_id)


# SERIALIZATION / DESERIALIZATION
def serialize_friends_list(friends_list):
    if friends_list != None:
        return quickle.dumps(friends_list)
    return None
def deserialize_friends_list(data):
    if data != None:
        return quickle.loads(data)
    return None

# FUNCTIONS
def add_to_friends_list(user, add_user):
    add_user = str(add_user)
    friends_list = deserialize_friends_list(user.friends)
    if friends_list != None:
        exists = False
        for friend in friends_list:
            if friend == add_user:
                exists = True
                break
        if not exists:
            friends_list.append(add_user)
    else:
        friends_list = [add_user]
    user.friends = serialize_friends_list(friends_list)
    user.save()

def remove_from_friends_list(user, remove_user):
    remove_user = str(remove_user)
    friends_list = deserialize_friends_list(user.friends)
    if friends_list != None:
        exists = False
        for friend in friends_list:
            if friend == remove_user:
                exists = True
                break
        if exists:
            new_friends_list = []
            for friend in friends_list:
                if friend != remove_user:
                    new_friends_list.append(friend)
            user.friends = serialize_friends_list(new_friends_list)
            user.save()

def is_friends_with(data, user_id):
    friends = False
    friends_list = deserialize_friends_list(data)
    if friends_list != None:
        for friend in friends_list:
            if friend == str(user_id):
                friends = True
                break
    return friends



