import json
from time import sleep

from django.db.models import Count, Q, Max, Min
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product, Category, Discount
from apps.products.serializers import ProductSerializer, ProductSerializer2
from .get_data import get_products_field, attributes_in_category, filtered_products, filters_in_category, options_in_category, get_all_category_children, \
    get_all_products_in_category_or_all
from unine_engine.globals import PRODUCTS_SORTING, PRODUCTS_PER_PAGE


def catalog(request):
    result_request = {
        "categories": Category.get_all_categories(),
    }
    return render(request, 'products/catalog.html', result_request)


# TODO Доробити
def specials(request):
    _products = Discount.objects.values_list('product_fk_id', flat=True).filter(product_fk__active=True,
                                                                                end_date__gt=now()
                                                                                )
    page = request.GET.get('page', 1)
    temp_products_paginator = None
    if type(page) != int and len(page.split(',')) > 0:
        page_array = page.split(',')
        products, _products_paginator = get_products_field(products_ids=_products, limit=PRODUCTS_PER_PAGE, page=page_array[0], with_options=True, sorting=None)
        for index, page in enumerate(page_array):
            if index == 0:
                continue
            temp_products, temp_products_paginator = get_products_field(products_ids=_products, limit=PRODUCTS_PER_PAGE, page=page, with_options=True)
            products.extend(temp_products)
    else:
        products, _products_paginator = get_products_field(products_ids=_products, limit=PRODUCTS_PER_PAGE, page=request.GET.get('page', 1), with_options=True, sorting=None)

    result_request = {
        "products": products,
        "products_paginator": temp_products_paginator if temp_products_paginator else _products_paginator,
    }

    return render(request, 'products/specials.html', result_request)


# TODO Доробити
def search(request):
    query = request.GET.get('query', None)
    page = request.GET.get('page', 1)
    sorting = request.GET.get('sorting', PRODUCTS_SORTING[0][0])
    _products = get_all_products_in_category_or_all()
    min_price = _products.price_min
    max_price = _products.price_max
    filters_json = json.loads(request.GET.get('filter_json', "{}"))
    if 'min_price' not in filters_json:
        filters_json['min_price'] = min_price
        filters_json['max_price'] = max_price
    if 'query' not in filters_json:
        filters_json['query'] = query
    if filters_json and ('min_price' in filters_json
                         or 'attributes_id' in filters_json
                         or 'options_id' in filters_json
                         or 'filters_id' in filters_json
                         or len(filters_json['attributes_id']) > 0
                         or len(filters_json['options_id']) > 0):
        _products = filtered_products(filters_json)

    temp_products_paginator = None
    if type(page) != int and len(page.split(',')) > 0:
        page_array = page.split(',')
        products, _products_paginator = get_products_field(_products, limit=PRODUCTS_PER_PAGE, page=page_array[0], with_options=True)
        for index, page in enumerate(page_array):
            if index == 0:
                continue
            temp_products, temp_products_paginator = get_products_field(_products, limit=PRODUCTS_PER_PAGE, page=page, with_options=True)
            products.extend(temp_products)
    else:
        products, _products_paginator = get_products_field(_products, limit=PRODUCTS_PER_PAGE, page=request.GET.get('page', 1), with_options=True)

    attributes = attributes_in_category(None, filters_json['attributes_values_id'] if 'attributes_values_id' in filters_json else [])
    filters = filters_in_category(None, filters_json['filters_values_id'] if 'filters_values_id' in filters_json else [])
    options = options_in_category(None, filters_json['options_values_id'] if 'options_values_id' in filters_json else [])

    result_request = {
        'selected_sorting': sorting,
        "category_attributes": attributes,
        "category_filters": filters,
        "category_options": options,
        "categories_main": Category.get_all_categories(is_parents=False),
        "products": products,
        "products_paginator": temp_products_paginator if temp_products_paginator else _products_paginator,
        "category_max_price": max_price,
        "category_min_price": min_price,
        "query": query,
        "max_price": filters_json['max_price'] if 'max_price' in filters_json else max_price,
        "min_price": filters_json['min_price'] if 'min_price' in filters_json else min_price,
    }
    return render(request, 'products/search.html', result_request)


# TODO Доробити
@csrf_exempt
def product_or_category(request, category_product_link):
    category_slugs = [str(x) for x in category_product_link.split('/')]
    try:
        product = Product.get_product_by_link(category_slugs[-1])
        if product.redirect or product.get_absolute_url() != request.path:
            return redirect(product.get_absolute_url())
        context = {
            "product": product,
        }
        return render(request, 'products/product.html', context)
    except Exception as ex:
        print('Product error:', ex)

    try:
        page = request.GET.get('page', 1)
        sorting = request.GET.get('sorting', PRODUCTS_SORTING[0][0])

        category_slugs.append(category_slugs[-1])  # Додаю до категорій останню категорію тому що це не продукт
        category = Category.get_category_by_link(category_slugs[-1])

        """ Якщо ссилка в іншій мові відрізняється то перейти на неї """
        if category.redirect:
            return redirect(category.get_absolute_url())

        _products = get_all_products_in_category_or_all(category.id)
        min_price = _products.price_min
        max_price = _products.price_max

        # TODO створення нових фільтрів
        filters_json = json.loads(request.GET.get('filter_json', "{}"))
        if filters_json and (
                'min_price' in filters_json or
                'attributes_id' in filters_json or
                'options_id' in filters_json or
                'filters_id' in filters_json or
                len(filters_json['attributes_id']) > 0 or
                len(filters_json['options_id']) > 0):
            filters_json['category_id'] = category.id

            _products = filtered_products(filters_json)

        attributes = attributes_in_category(category.id, filters_json['attributes_values_id'] if 'attributes_values_id' in filters_json else [])
        filters = filters_in_category(category.id, filters_json['filters_values_id'] if 'filters_values_id' in filters_json else [])
        options = options_in_category(category.id, filters_json['options_values_id'] if 'options_values_id' in filters_json else [])
        # TODO створення нових фільтрів
        import time
        start_time = time.time()

        temp_products_paginator = None
        if type(page) != int and len(page.split(',')) > 0:
            page_array = page.split(',')
            products, _products_paginator = get_products_field(_products, limit=PRODUCTS_PER_PAGE, sorting=sorting, page=page_array[0], with_options=True)
            for index, page in enumerate(page_array):
                if index == 0:
                    continue
                temp_products, temp_products_paginator = get_products_field(_products, limit=PRODUCTS_PER_PAGE, sorting=sorting, page=page, with_options=True)
                products.extend(temp_products)
        else:
            products, _products_paginator = get_products_field(_products, limit=PRODUCTS_PER_PAGE, sorting=sorting, page=page, with_options=True)
        print("--- %s OLD seconds ---" % (time.time() - start_time))

        result_request = {
            'selected_sorting': sorting,
            "category": category,
            "category_attributes": attributes,
            "category_filters": filters,
            "category_options": options,
            "categories_children": get_all_category_children(category.id),
            "categories_main": Category.get_all_categories(is_parents=False),
            "products": products,
            "products_paginator": temp_products_paginator if temp_products_paginator else _products_paginator,
            "category_max_price": max_price,
            "category_min_price": min_price,
            "max_price": filters_json['max_price'] if 'max_price' in filters_json else max_price,
            "min_price": filters_json['min_price'] if 'min_price' in filters_json else min_price,
        }
        return render(request, 'products/category.html', result_request)
    except Exception as ex:
        print("not category or error", ex)
    # print('ERROR: def product_or_category(request, category_link, product_link):')
    raise Http404("NotProductAndNOtCategory")

# class ProductGenericView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer2
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         author = get_object_or_404(Product, id=self.request.data.get('id'))
#         return serializer.save(author=author)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class ProductView(APIView):
#     def get(self, request):
#         products = Product.objects.all()[:10]
#         serializer = ProductSerializer(products, many=True)
#         return Response({'articles': serializer.data})
#
#     def post(self, request):
#         product = request.data.get('product')
#         serializer = ProductSerializer(data=product)
#         if serializer.is_valid(raise_exception=True):
#             saved = serializer.save()
#         return Response({'success': True})
#
#     def put(self, request, id):
#         saved_product = get_object_or_404(Product.objects.all(), id=id)
#         data = request.data.get('product')
#         serializer = ProductSerializer(instance=saved_product, data=data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             saved = serializer.save()
#         return Response({'success': True})
#
#     def delete(self, request, id):
#         product = get_object_or_404(Product.objects.all(), id=id)
#         product.delete()
#         return Response({'success': True})
