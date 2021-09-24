from django.http import FileResponse, Http404


from ScratchBowling.sbs_utils import is_valid_uuid
from ScratchBowling.websettings import WebSettings
from tournaments.models import Sponsor
from tournaments.tournament_utils import get_tournament


def get_sponsor_pic(request, id):
    id = is_valid_uuid(id)
    if id != None:
        sponsor = Sponsor.objects.filter(sponsor_id=id).first()
        if sponsor != None:
            settings = WebSettings()
            img = open(settings.os_path + 'media/' + str(sponsor.sponsor_image), 'rb')
            if img != None:
                return FileResponse(img)

    img = open(settings.os_path + 'media/sponsor-pictures/default.png', 'rb')
    if img != None:
        return FileResponse(img)
    else:
        return Http404('Could not find sponsor picture specified.')



def get_tournament_pic(request, id):
    tournament = get_tournament(id)
    if tournament != None:
        settings = WebSettings()
        img = open(settings.os_path + 'media/' + str(tournament.picture), 'rb')
        if img != None:
            return FileResponse(img)
        else:
            img = open(settings.os_path + 'media/tournament-pictures/default.jpg', 'rb')
            if img != None:
                return FileResponse(img)
            else:
                return Http404('Could not find winners picture specified.')