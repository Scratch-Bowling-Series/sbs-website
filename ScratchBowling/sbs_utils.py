import uuid


def is_valid_uuid(val):
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None
