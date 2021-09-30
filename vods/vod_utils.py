from ScratchBowling.sbs_utils import is_valid_uuid
from vods.models import Vod


def get_vod_url(vod_id):
    vod_id = is_valid_uuid(vod_id)
    if vod_id != None:
        vod = Vod.objects.filter(vod_id=vod_id).first()
        if vod != None:
            return '/media/' + vod.video
    return '/media/vods/default.mp4'