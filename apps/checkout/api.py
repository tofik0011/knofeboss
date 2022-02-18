import base64
import json
from datetime import datetime

from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from liqpay import LiqPay

from mainapp.helper import validate_email, validate_phone, trim_phone
from .get_data import get_cart, render_cart_items, render_cart_item
from apps.products.get_data import get_options_of_product_objects_by_ids, get_product_with_certain_options
from django.views.decorators.csrf import csrf_exempt
from .models import OptionOfProduct, Order, OrderStatus, CartItem
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from ..currency.models import Currency
from ..currency.views import currency_get, convert_price

from ..currency.views import currency_get, convert_price, get_currency_data_for_order
from ..email_notifications.views import notify_admin_about_order
from ..products.models import Product


def send_liqpay(request):
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    order_id = request.session['order_id']
    currency = request.session['currency_code']
    try:
        order = Order.objects.get(id=order_id)
    except Exception as ex:
        return redirect(reverse('index'))
    print('Eto LiQPaY detka')
    form_l = {
        "action": "pay",
        "amount": str(order.get_total_price()),
        "currency": currency,
        "description": f'Заказ №{order.id}',
        "order_id": order_id,
        "result_url": 'https://' + request.get_host() if request.is_secure() else 'http://' + request.get_host(),
        "version": "3",
        "server_url": 'https://' + request.get_host() + reverse('get_liqpay') if request.is_secure() else 'http://' + request.get_host() + reverse('get_liqpay'),
    }
    print(form_l)
    html = liqpay.cnb_form(form_l)
    return html


@csrf_exempt
def get_liqpay(request):
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    data = request.POST.get('data')
    signature = request.POST.get('signature')
    sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
    print(signature)
    print(sign)
    if sign == signature:
        print('callback is valid')
        response = json.loads(base64.b64decode(data).decode('utf-8'))
        print(response['order_id'])
        order = Order.objects.get(id=response['order_id'])
        if response['status'] == "success" or response['status'] == "sandbox":
            order.is_paid = True
            order.save()
        if response['status'] == "reversed":
            order.is_paid = False
            order.save()
        print(response['status'])
        print('callback data', response)
    return HttpResponse()


def get_option_of_product_by_product_id(request):
    data = list()
    product_id = request.GET.get('product_id', None)
    option_ids = request.GET.get('option_ids', None)
    if product_id:
        option_of_product = OptionOfProduct.objects.filter(product_fk_id=product_id).order_by('option_fk_id', 'option_value_fk_id')

        for oop in option_of_product:
            data.append({
                'id': oop.id,
                'product_id': oop.product_fk_id,
                'option_id': oop.option_fk_id,
                'option_value_id': oop.option_value_fk_id,
                'option_build_name': oop.__str__(),
            })
        data = sorted(data, key=lambda k: k['option_build_name'], reverse=True)
    return JsonResponse(data, safe=False)


def render_quick_order_item(request):
    product_id = request.POST.get('product_id')
    options_ids = json.loads(request.POST.get('options', []))
    product_obj = Product.objects.get(id=product_id)
    options_obj = get_options_of_product_objects_by_ids(product_id, options_ids)
    check_for_required_options = product_obj.check_for_required_options(options_obj)
    if check_for_required_options is True:
        _data = get_product_with_certain_options(product=product_obj, user_id=request.user.id, options=options_obj)
        return JsonResponse({'success': True, 'html': render_to_string('checkout/quick_order_item.html', {'success': True, 'data': _data, 'request': request})})
    else:
        return JsonResponse({'success': False, 'error': 'no_required', 'required': list(check_for_required_options)})


def change_item_qty(request):
    cart = get_cart(request)
    response = cart.change_item_qty(request.user.id, request.POST.get('item_id'),
                                    json.loads(request.POST.get('operation')))
    print(response)
    if response['success']:
        return JsonResponse({'success': True,
                             'cart_items_count': round(response['cart_items_count']),
                             'cart_item_html': render_cart_item(request.POST.get('item_id'), request),
                             'cart_total_price': convert_price(request, response['cart_total_price']),
                             })
    else:
        return JsonResponse({'success': False})


def add_to_cart(request):
    cart = get_cart(request)
    product_id = request.POST.get('product_id')
    options = json.loads(request.POST.get('product_options', '[]'))
    qty = request.POST.get('qty', 1)
    options_obj = OptionOfProduct.objects.none()
    if options:
        options_obj = get_options_of_product_objects_by_ids(product_id, options)
    response = cart.add_item_to_cart(_product_id=product_id, _user_id=request.user.id, _options=options_obj, _qty=qty)
    notification_data = {'heading': _('checkout__added_to_cart_notification'),
                         'icon': 'bag_filled',
                         'buttons': [
                             {'link': reverse('view__checkout'),
                              'class': 'btn_v1',
                              'text': "Оформить заказ"},
                             {'link': '#',
                              'class': 'btn_v2 close_ntf',
                              'text': "Продолжить покупки"},
                         ]}
    notification = render_to_string('mainapp/parts/custom_notification.html', notification_data)
    if response['success']:
        return JsonResponse({'success': True, 'cart_items_count': response['cart_items_count'], 'cart_total_price': convert_price(request, response['cart_total_price'], with_code=True),
                             'render_html': render_cart_items(request),
                             'notification': notification})
    elif not response['success'] and 'required' in response:
        return JsonResponse({'success': False, 'message': _('checkout__select_required_options'), 'required': list(response['required'])})
    elif not response['success']:
        return JsonResponse({'success': False, 'message': response['message']})


def remove_from_cart(request):
    cart = get_cart(request)
    cart_item_id = request.POST.get('cart_item_id')
    response = cart.remove_item_from_cart(cart_item_id)
    if response['success']:
        return JsonResponse({'success': True, 'cart_items_count': round(response['cart_items_count']),
                             'cart_total_price': convert_price(request, response['cart_total_price']),
                             })
    else:
        return JsonResponse({'success': False})


# TODO cart item fk
@csrf_exempt
def add_one_click_order(request):
    try:
        first_name = request.POST.get('first_name', '')
        comment = request.POST.get('comment', '')
        options = request.POST.get('product_options', [])
        product_id = request.POST.get('product_id', None)
        phone = trim_phone(request.POST.get('phone', None))
        if not validate_phone(phone):
            return JsonResponse({'success': False, 'message': _("error__invalid_phone")})
        product = Product.objects.get(id=product_id)
        options_obj = get_options_of_product_objects_by_ids(product_id, options)
        user = request.user if request.user.is_authenticated else None
        order = Order.objects.create(user=user, first_name=first_name, phone=phone, comment=comment, is_one_click_order=True)
        cart = get_cart(request)
        cart.flush_items()
        cart.refresh_fields()
        cart.add_item_to_cart(_product_id=product_id, _user_id=request.user.id, _options=options_obj, _qty=product.min_unit)
        cart.items.update(order_fk_id=order.id)
        order.total = order.get_total_price()
        order.currency_data = get_currency_data_for_order(request)
        order.save(add_order_status=True)
        cart.flush_items()
        cart.refresh_fields()
        notify_admin_about_order(order, request)

    except Exception as e:
        print(str(e))
        return JsonResponse({'success': False, 'message': _('unknown_error')})
    return JsonResponse({'success': True, 'message': _('checkout__bioc_success_message')})
