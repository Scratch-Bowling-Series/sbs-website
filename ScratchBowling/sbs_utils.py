import os
import uuid

from ScratchBowling.websettings import WebSettings


def is_valid_uuid(val):
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None


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
