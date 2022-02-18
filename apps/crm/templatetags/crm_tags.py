from __future__ import unicode_literals
from django import template
from django.urls import reverse
import urllib

register = template.Library()


@register.simple_tag
def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urllib.urlencode(get)
    return url
