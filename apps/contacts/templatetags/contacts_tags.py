from __future__ import unicode_literals
from django import template
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext as _, get_language
import json
from apps.contacts.models import Phone, SocialNetwork, Email, Address

register = template.Library()


@register.simple_tag
def tag_get_emails(all=True):
    emails = Email.objects.values_list('email', named=True).order_by('order')
    return emails if all else emails.first()


@register.simple_tag
def tag_get_all_phones():
    return Phone.objects.all().order_by('order')


@register.simple_tag
def tag_get_phone_by_keyword(keyword):
    return Phone.objects.filter(keyword=keyword).first()


@register.simple_tag
def tag_get_addresses(all=True):
    address = Address.objects.values_list('address', named=True).filter(language=get_language()).order_by('order')
    return address if all else address.first()


@register.simple_tag
def tag_get_socials_networks():
    objects = SocialNetwork.objects.all()
    res = {}
    for obj in objects:
        res[obj.keyword] = obj.link
    return res
