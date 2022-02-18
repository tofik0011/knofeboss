from __future__ import unicode_literals
from django import template
from django.utils.translation import ugettext as _, get_language
from apps.banner.models import Banner

register = template.Library()


@register.simple_tag
def tag_get_banner(kw):
    try:
        banner = Banner.objects.filter(active=True, keyword=kw).last()
        return banner
    except Exception as ex:
        return ""


