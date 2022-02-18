from __future__ import unicode_literals

from collections import OrderedDict

from mainapp.models import Settings
from unine_engine import globals
from django import template
from django.utils.timezone import now
from unine_engine.globals import PRODUCTS_SORTING
from apps.profile.models import Profile
from apps.products_comparison.views import get_comparison
from apps.products.get_products import get_latest_products, get_specials_products, get_visited_products, get_popular_products, get_random_products
from django.utils.translation import ugettext as _, get_language
from django.conf import settings
from ..get_data import get_products_field
from apps.products.models import Product

register = template.Library()


@register.simple_tag
def tag_get_similar_products(request, product_id):
    product = Product.objects.get(id=product_id)
    similar = product.similar.all()
    for pr in similar:
        pr.price_data = pr.get_price(request.user.id)
    return similar


@register.simple_tag
def tag_check_product_current_status(request, product_id):
    """Провіряє чи продукт знаходиться в списку бажань або в порівнянні товарів"""
    comparison = get_comparison(request)
    res = dict()
    res['in_comparison'] = comparison.has_product(product_id)
    try:
        if request.user.is_authenticated:
            account = Profile.objects.get(id=request.user.id)
            res['in_wishlist'] = account.has_in_wishlist(product_id)
        else:
            res['in_wishlist'] = False
    except Exception as ex:
        print('tag_check_product_current_status: ', str(ex))
        res['in_wishlist'] = False
    return res


@register.filter
def filter_plus(num1, num2):
    return num1 + num2


@register.filter
def filter_discount_day_timer(end_date):
    past = end_date.day - now().day
    if past > 0:
        return f"{_('products__days_to_discount_end')}: {past}"
    else:
        return f"{_('products__discount_end_today')}"


@register.filter
def filter_minus(num1, num2):
    return num1 - num2


@register.simple_tag
def tag_get_visited_products(request, current_product_id, limit=5):
    ids = request.session.get('visited_products', None)
    return get_visited_products(ids, current_product_id, qty=limit) if ids else None


@register.simple_tag
def tag_get_products(keyword="latest", limit=8):
    if keyword == 'latest':
        return get_latest_products(qty=limit)
    if keyword == 'popular':
        return get_popular_products(qty=limit)
    if keyword == 'random':
        return get_random_products(qty=limit)
    if keyword == 'specials':
        get_specials_products(qty=limit)


@register.simple_tag
def tag_get_sorting_list():
    return PRODUCTS_SORTING


@register.simple_tag
def tag_count_visited_product(request, product_id):
    products = request.session.get('visited_products', [])
    products = list(OrderedDict.fromkeys(products))
    request.session['visited_products'] = products
    if len(products) > globals.VISITED_PRODUCTS_LIMIT:
        del products[0]
    products.append(product_id)


@register.filter
def filter_image_x2(value, x=2):
    """Фільтер для збільшеня width/height картинки в 2 рази"""
    if value:
        return int(value) * x
    else:
        return None

@register.simple_tag
def tag_generation_product_title(product):
    setting_seo_title = Settings.objects.first()
    vars = {
        'name': product.name,
        'description': product.description,
        'price': product.calc_price,
    }
    text = setting_seo_title.formula_for_seo_generation_title
    for i in vars.keys():
        text = text.replace(f'<{i}>', str(vars[i]))
    return text

@register.simple_tag
def tag_generation_product_description(product):
    setting_seo_discription = Settings.objects.first()
    vars = {
        'name': product.name,
        'description': product.description,
        'price': product.calc_price,
    }
    text = setting_seo_discription.formula_for_seo_generation_description
    for i in vars.keys():
        text = text.replace(f'<{i}>', str(vars[i]))
    return text