from django.urls import path
from .api import get_option_of_product_by_product_id, send_liqpay, get_liqpay, change_item_qty, add_to_cart, remove_from_cart, add_one_click_order, render_quick_order_item
from .views import *

urlpatterns = [
    path('checkout/', Checkout.as_view(), name="view__checkout"),
    path('api/get_option_of_product_by_product_id/', get_option_of_product_by_product_id, name="get_option_of_product_by_product_id"),
    path('api/send_liqpay/', send_liqpay, name="send_liqpay"),
    path('api/get_liqpay/', get_liqpay, name="get_liqpay"),
    path('api/add_one_click_order/', add_one_click_order, name="add_one_click_order"),
    path('api/change_item_qty/', change_item_qty, name='change_item_qty'),
    path('api/add_to_cart/', add_to_cart, name='add_to_cart'),
    path('api/remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('liqpay_success/', liqpay_success_page, name="liqpay_success_page"),
    path('api/render_one_click_order_item/', render_quick_order_item, name='render_quick_order_item'),
]
