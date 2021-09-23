import quickle
from ScratchBowling.sbs_utils import is_valid_uuid
from oils.models import Oil_Pattern



def get_oil_pattern_data(uuid):
    uuid = is_valid_uuid(uuid)
    if uuid is not None:
        data = Oil_Pattern.objects.filter(pattern_id=uuid).first()
        if data != None:
            data = data.pattern_cache
            if data != None:
                return quickle.loads(data)
    return None

def get_oil_display_data(display_id):
    data = Oil_Pattern.objects.filter(pattern_db_id=display_id).first()
    if data != None:
        data = data.pattern_cache
        if data != None:
            return quickle.loads(data)
    return None

