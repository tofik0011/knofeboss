import numpy
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _, get_language
from apps.checkout.models import CartItem
from apps.products.get_data import get_products_field
from apps.products.models import Product, Discount
from unine_engine.globals import PRODUCTS_PER_PAGE, PRODUCTS_SORTING


def get_visited_products(visited_ids, current_id, qty=8):
    products = Product.objects.filter(active=True, id__in=visited_ids).exclude(
        id=current_id)[:qty]
    data, paginator = get_products_field(products=products, limit=qty, with_options=True, sorting='-added_date')
    return data


def get_popular_products(qty=8):
    products = Product.objects.annotate(popularity=Count('id')).filter(cartitem__order_fk__isnull=False)
    data, paginator = get_products_field(products=products, limit=qty, with_options=True)
    return data


def get_random_products(qty=8):
    all_ids = Product.objects.values_list('id', flat=True).all()
    if qty > all_ids.count():
        qty = all_ids.count()
    product_ids = numpy.random.choice(all_ids, size=qty, replace=False)
    data, paginator = get_products_field(products_ids=product_ids, with_options=True)
    return data


def get_latest_products(qty=8):
    products = Product.objects.filter(active=True)
    data, paginator = get_products_field(products=products, limit=qty, with_options=True, sorting='-added_date')
    return data


def get_specials_products(qty=16):
    products = Discount.objects.values_list('product_fk_id', flat=True).filter(product_fk__active=True, end_date__gt=now()).order_by('-product_fk__added_date')[:qty]
    products = list(products)
    if len(products) % 2 == 1:
        products = products[:-1]
    data, paginator = get_products_field(products_ids=products, limit=qty, with_options=True)
    return data
