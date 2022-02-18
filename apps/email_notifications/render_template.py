from django.template.loader import render_to_string
from mainapp.models import Settings
from unine_engine.globals import DELIVERY_CHOICES, PAYMENT_CHOICES


def render_order_to_buyer(_order, request):
    _items = _order.cartitem_set.all()
    try:
        delivery_type = dict(DELIVERY_CHOICES)[_order.delivery_type]
        payment_type = dict(PAYMENT_CHOICES)[_order.payment_type]
    except Exception as e:
        delivery_type = ''
        payment_type = ''
    try:
        logo = Settings.objects.first().logo
    except Exception as e:
        logo = ''

    site = {
        'name': 'CROCUS',
        'link': 'site_link',
        'image': logo,
    }
    customer = {
        'first_name': _order.first_name,
        'last_name': _order.last_name,
        'phone': _order.phone,
        'email': _order.email,
    }

    order = {
        'date': _order.date,
        'number': _order.id,
        'delivery_address': _order.delivery_address,
        'delivery_type': delivery_type,
        'payment_type': payment_type,
        'total_price': _order.total,
    }
    items = []

    for item in _items:
        # product_fields = get_product_field(item.product_fk.id)
        image_url = 'https://' + request.get_host() + item.product_fk.image.url

        items.append({
            'name': item.product_fk.name,
            'link': item.product_fk.get_absolute_url(),
            'image': image_url,
            'qty': item.qty,
            'article': item.product_fk.article,
            'total_price': item.product_fk.price

        })

    data = {
        'items': items,
        'site': site,
        'customer': customer,
        'order': order,
    }
    return render_to_string('email_notifications/checkout__order_to_buyer.html', data)


def render_order_to_admin(_order, request):
    _items = _order.cartitem_set.all()
    try:
        delivery_type = dict(DELIVERY_CHOICES)[_order.delivery_type]
        payment_type = dict(PAYMENT_CHOICES)[_order.payment_type]
        logo = Settings.objects.first().logo
    except Exception as e:
        delivery_type = ''
        payment_type = ''
        logo = ''
    site = {
        'name': 'CROCUS',
        'link': 'site_link',
        'image': logo,
    }
    customer = {
        'first_name': _order.first_name,
        'last_name': _order.last_name,
        'phone': _order.phone,
        'email': _order.email,
    }

    order = {
        'date': _order.date,
        'number': _order.id,
        'delivery_address': _order.delivery_address,
        'delivery_type': delivery_type,
        'payment_type': payment_type,
        'total_price': _order.total,
    }
    items = []

    for item in _items:

        # product_fields = get_product_field(item.product_fk.id)
        image_url = 'https://' + request.get_host() + item.product_fk.image.url

        items.append({
            'name': item.product_fk.name,
            'link': item.product_fk.get_absolute_url(),
            'image': image_url,
            'qty': item.qty,
            'article': item.product_fk.article,
            'total_price': item.product_fk.price

        })

    data = {
        'items': items,
        'site': site,
        'customer': customer,
        'order': order,
    }
    print(data)
    return render_to_string('email_notifications/checkout__order_to_admin.html', data)
