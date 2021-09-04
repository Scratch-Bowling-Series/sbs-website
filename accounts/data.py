from django.http import FileResponse, Http404

from ScratchBowling.sbs_utils import is_valid_uuid
from ScratchBowling.views import User
from ScratchBowling.websettings import WebSettings


def get_profile_pic(request, id):
    id = is_valid_uuid(id)
    user = User.objects.filter(user_id=id).first()
    if user != None:
        settings = WebSettings()
        img = open(settings.os_path + 'media/' + str(user.picture), 'rb')
        if img != None:
            return FileResponse(img)
        else:
            img = open(settings.os_path + 'media/profile-pictures/default.jpg', 'rb')
            if img != None:
                return FileResponse(img)
            else:
                return Http404('Could not find profile picture specified.')
