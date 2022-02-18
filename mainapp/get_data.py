from django.template.loader import render_to_string
from django.utils.translation import get_language
from .models import Settings
from apps.menu.models import MenuItem


# TODO трохи переписати
def render_menu(keyword):
    pass


def get_settings():
    s, c_s = Settings.objects.get_or_create(defaults={'robots_txt': 'User-agent: *\nDisallow: /'})
    return s
