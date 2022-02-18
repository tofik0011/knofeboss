from __future__ import unicode_literals
from django import template
from apps.currency.models import Currency
from apps.currency.views import currency_set_and_get, get_all_currencies, convert_price
import json

register = template.Library()


@register.simple_tag
def tag_get_all_currencies_json(request):
    currency_set_and_get(request)
    result = get_all_currencies()
    return json.dumps(list(result.values()), ensure_ascii=False, default=str)


@register.simple_tag
def tag_get_all_currencies(request):
    currency_set_and_get(request)
    return get_all_currencies()


@register.simple_tag
def tag_currency_get(request):
    return request.session['currency_code']


@register.simple_tag
def tag_current_currency_json(request):
    currency = Currency.objects.values().get(code=request.session['currency_code'])
    return json.dumps(dict(currency), ensure_ascii=False, default=str)


@register.simple_tag
def tag_default_currency_json():
    currency = Currency.objects.values().get(is_default=True)
    return json.dumps(dict(currency), ensure_ascii=False, default=str)


@register.simple_tag
def tag_convert_currency_price(request, price, with_code=True):
    return convert_price(request, price, with_code)
