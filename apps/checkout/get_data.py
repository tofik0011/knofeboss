from django.template.loader import render_to_string
from apps.checkout.models import Cart, CartItem


def get_cart(request):
    if request.user.is_authenticated:
        profile = request.user
        if profile.cart is None:
            cart = Cart.objects.create()
            profile.cart = cart
            profile.save()
        return profile.cart
    else:
        try:
            cart_id = request.session['cart_id']
            cart = Cart.objects.get(id=cart_id)
        except Exception as e:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            request.session['cart_id'] = cart_id
            cart = Cart.objects.get(id=cart_id)
        return cart


def render_cart_items(request):
    cart = get_cart(request)
    cart_items = cart.items.all()
    cart_total_price = cart.total_price
    res = {
        'checkout': render_to_string('checkout/cart_items_checkout.html',
                                     {'cart_items': cart_items, 'cart_total_price': cart_total_price}, request),
        'dropdown': render_to_string('mainapp/parts/cart_dropdown.html',
                                     {'cart_items': cart_items, 'cart_total_price': cart_total_price}, request)
    }
    return res


def render_cart_item(cart_item_id, request):
    res = {}
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
    except Exception as e:
        print(str(e))
        return None
    res["checkout"] = render_to_string('checkout/cart_item.html', {'item': cart_item, 'request': request})
    res["dropdown"] = render_to_string('checkout/cart_item_dropdown.html', {'item': cart_item, 'request': request})
    return res