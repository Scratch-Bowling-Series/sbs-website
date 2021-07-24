import uuid

from django.contrib.auth import get_user_model

User = get_user_model()

def get_name_from_uuid(uuid):
    uuid = is_valid_uuid(uuid)
    if uuid is not None:
        user = User.objects.filter(user_id=uuid).first()
        if user is not None:
            return user.first_name + ' ' + user.last_name



def is_valid_uuid(val):
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None