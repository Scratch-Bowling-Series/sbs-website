import string
import random

from django import template

register = template.Library()

@register.simple_tag
def session_id(input):
    return '#' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

@register.simple_tag
def web_version(input):
    return 'v1.3.525-beta'