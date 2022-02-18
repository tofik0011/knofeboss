from django.contrib import admin
from django.urls import path, include, re_path
from apps.checkout.views import *
from apps.products.get_data import get_product_price_by_options, search_product_by_query, get_product_option_price
from .api import *
from .views import *

urlpatterns = [
    path('catalog/', catalog, name="catalog"),
    path('specials/', specials, name="specials"),
    path('search/', search, name="view__search"),
    # re_path(r'^api/products/', ProductView.as_view(), name='products'),
    re_path(r'^catalog/(?P<category_product_link>.+)/$', product_or_category, name='product_or_category'),
    re_path(r'^api/add_review/$', add_review, name='add_review'),
    re_path(r'^api/load_more_reviews/$', load_more_reviews, name='load_more_reviews'),
    re_path(r'^api/get_template_product_cart/$', get_template_product_cart, name='get_template_product_cart'),
    re_path(r'^api/get_template_products_cart/$', get_template_products_cart, name='get_template_products_cart'),
    re_path(r'^api/search/$', search_product_by_query, name='search_product_by_query'),
    re_path(r'^j/get_product_price_by_options/$', get_product_price_by_options, name='get_product_price_by_options'),
    re_path(r'^api/get_product_option_price/$', get_product_option_price, name='get_product_option_price'),
    re_path(r'^api/get_template_catalog/$', get_template_catalog, name='get_template_catalog'),
    # Для адмінки
    re_path(r'^api/get_attribute_values_id_by_attribute_id_json/$', get_attribute_values_id_by_attribute_id_json, name='get_attribute_values_id_by_attribute_id_json'),
    re_path(r'^api/get_filter_values_id_by_filter_id_json/$', get_filter_values_id_by_filter_id_json, name='get_filter_values_id_by_filter_id_json'),
    re_path(r'^api/get_option_values_id_by_option_id_json/$', get_option_values_id_by_option_id_json, name='get_option_values_id_by_option_id_json'),
]
