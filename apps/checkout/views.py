from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.translation import ugettext_lazy as _
from django_currentuser.middleware import get_current_user, get_current_authenticated_user

from apps.checkout.forms import CheckoutForm
from apps.checkout.get_data import get_cart
from apps.checkout.models import Order
from apps.products.models import *
from unine_engine.globals import PAYMENT_CHOICES, DELIVERY_CHOICES


def liqpay_success_page(request):
    return render(request, 'checkout/order_success_liqpay.html')


class Checkout(View):

    def get(self, request):
        cart = get_cart(request)
        cart.refresh_fields()
        return render(request, 'checkout/checkout.html', {'payment_types': PAYMENT_CHOICES, 'delivery_types': DELIVERY_CHOICES})

    def post(self, request):
        cart = get_cart(request)
        if cart.items.all().count() == 0:
            return JsonResponse({'success': False, 'message': _('checkout__cart_is_empty')})
        res = Order.validate_order_form(request.POST)
        if res['success']:
            order = Order.add_order(request.POST, request, cart)
            if order['payment'] is False:
                return JsonResponse({'success': True,"redirect": reverse("index"), 'message': _('checkout__order_success_message')})
            else:
                return  JsonResponse(order)
        else:
            return JsonResponse(res)



def add_order_success(request, **kwargs):
    if kwargs['liqpay'] == 'True':
        return render(request, 'checkout/order_success_liqpay.html')
    else:
        return render(request, 'checkout/order_success.html')

