from decimal import Decimal

from django import template
from django.template.loader import render_to_string
from django.conf import settings
from apps.checkout.api import get_cart
from ..models import Order
from apps.checkout.get_data import render_cart_items

register = template.Library()


@register.simple_tag
def tag_render_cart_items_html(request):
    return render_cart_items(request)


@register.simple_tag
def tag_get_cart_data(request):
    cart = get_cart(request)
    cart_items = cart.items.all()
    res = {
        'cart_total_price': cart.total_price,
        'cart_items_count': cart.items_count,
        'cart_items': cart_items,
    }
    return res


@register.filter
def value_payment_type(name):
    name = dict(settings.PAYMENT_CHOICES)[name]
    return name


@register.simple_tag
def tag_order_history_currency_price(price, currency_data, with_code=True):
    try:
        currency_data = json.loads(currency_data.replace("'", '"'))
        if with_code:
            return f'{currency_data["symbol_left"]}{round(price * Decimal(currency_data["value"]), 2)} {currency_data["symbol_right"]}'
        else:
            return round(price * Decimal(currency_data["value"]), 2)
    except Exception as e:
        print('EX', str(e))
        return price
