import os

from django.http import Http404, FileResponse
from django.shortcuts import render

# Create your views here.
from ScratchBowling.sbs_utils import is_valid_uuid
from ScratchBowling.settings import MEDIA_ROOT
from ScratchBowling.websettings import WebSettings
from vods.models import Vod


def watch_views(request, id):
    return None


def poster_views(request, id):
    return None

