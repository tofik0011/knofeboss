import json
import operator
from decimal import Decimal
from functools import reduce
import numpy
from django.core.paginator import Paginator
from django.db.models import Count, Q, Max, Min, QuerySet
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import now
from unine_engine.globals import PRODUCTS_PER_PAGE, PRODUCTS_SORTING, PRODUCTS_SEARCH_BY_QUERY_LIMIT
from apps.products.models import Concat, AttributeOfProduct, Discount, OptionOfProduct, FilterOfProduct, Filter, FilterValue, Attribute, AttributeValue, Option, OptionValue
from .models import Category, Product
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from apps.currency.templatetags.currency_tags import convert_price


def get_products_field(products=None, products_ids=None, limit=None, page=1, with_options=False, sorting=PRODUCTS_SORTING[0][0]):
    if not limit:
        limit = PRODUCTS_PER_PAGE
    if products_ids is not None:
        products = Product.objects.filter(id__in=list(products_ids))
    if sorting is not None:
        products = products.order_by(sorting)

    products_paginator = Paginator(products, limit).page(page)
    data = []

    for product in products_paginator:
        discount = None
        if product.is_special:
            try:
                discount = product.get_product_discount()
                if discount and discount.end_date < timezone.now():
                    product.is_special = False
                    discount = None
                    product.save()
            except Exception as ex:
                pass
        is_new = now() - product.added_date
        # print('---------', product.is_special)
        temp = {
            'id': product.id,
            'qty': product.qty,
            'name': product.name,
            'is_bestseller': product.is_bestseller,
            'is_new': True if is_new.days < 14 else False,
            'category': product.category_fk,
            # 'calc_price': product.calc_price,
            # 'price': product.price,
            'rating': product.rating,
            'image': product.image,
            'link': product.get_absolute_url(),
            'options': product.options if with_options else None,
        }
        temp.update(product.get_price())
        data.append(temp)
    return data, products_paginator


def get_all_category_children(id):
    """ Віддає всіх дітей категорії """
    category = Category.objects.get(id=id)
    result = []
    for category in category.children.all():
        result.append({
            'category': category,
        })
    return result

def get_all_products_in_category_or_all(category_id=None):
    """ Віддає всі продукти в категорії """
    kwargs = {}
    if category_id:
        kwargs.update({'show_in_categories': category_id})
    _products = Product.objects.filter(active=True, **kwargs)

    _products.price_max = _products.aggregate(price_max=Max('calc_price'))['price_max']
    _products.price_min = _products.aggregate(price_min=Min('calc_price'))['price_min']
    return _products


def get_all_products_in_category_and_filter_attributes(category_id, _attributes, min_price=None, max_price=None):
    if _attributes:
        attr_val_temp = []
        for attr_val in _attributes:
            attr_val_temp.extend(attr_val['attribute_values'])
        attributes_of_product_temp = AttributeOfProduct.objects.filter(product_fk__active=True,
                                                                       product_fk__show_in_categories=category_id,
                                                                       attribute_fk__in=[attr['id'] for attr in _attributes],
                                                                       attribute_value_fk__in=[val['id'] for val in attr_val_temp])
        _products_pk = []
        _products_pk = sorted(set(attributes_of_product_temp.values_list('product_fk_id', flat=True)))

        filtered_products = AttributeOfProduct.objects.values('product_fk_id').annotate(
            attr=Concat('attribute_fk_id'),
            val=Concat('attribute_value_fk_id'),
            count=Count('product_fk_id'),
        ).filter(
            count=len(_attributes),
            attribute_value_fk_id__in=sorted([val['id'] for val in attr_val_temp]),
            product_fk__calc_price__gte=min_price,
            product_fk__calc_price__lte=max_price
        )
        products = filtered_products.values_list('product_fk_id', flat=True)
    else:
        products = Product.objects.values_list('id', flat=True).filter(
            active=True,
            show_in_categories=category_id,
            calc_price__gte=min_price,
            calc_price__lte=max_price
        )

    price = Product.objects.values('calc_price').filter(id__in=list(products), calc_price__gte=min_price, calc_price__lte=max_price).aggregate(
        price_max=Max('calc_price'), price_min=Min('calc_price')
    )
    products.price_max = price['price_max']
    products.price_min = price['price_min']
    return products


@csrf_exempt
def get_product_option_price(request):
    product_id = request.POST.get("product_id")
    option_id = request.POST.get("option_id")
    value_id = request.POST.get("value_id")
    return JsonResponse(Product.objects.get(id=product_id).get_product_option_price(option_id, value_id), safe=False)


def get_options_list_of_products(products_ids, filtered_products_ids):
    options_obj = OptionOfProduct.objects.filter(
        product_fk__active=True,
        product_fk_id__in=list(products_ids)
    )
    options_ids = set(options_obj.values_list('option_fk_id', flat=True))
    result = []
    for option in options_ids:
        option_lang = Option.objects.get(id=option)
        option_values_filtered = set(
            options_obj.values_list('option_value_fk_id', flat=True).filter(option_fk_id=option))
        result_option_values = list()

        for option_value in option_values_filtered:
            option_value_lang = OptionValue.objects.values_list('value', flat=True).get(id=option_value)
            result_option_values.append(
                {'id': option_value,
                 'option_id': option,
                 'name': option_value_lang,
                 'count_products': options_obj.filter(product_fk_id__in=filtered_products_ids, option_fk_id=option,
                                                      option_value_fk_id=option_value).count(),
                 'checked': 0,
                 })

        result.append({
            'option': {'id': option, 'name': option_lang.name},
            'option_values': result_option_values
        })
    return result


def get_attributes_list_of_products(products_ids, filtered_products_ids):
    attributes_obj = AttributeOfProduct.objects.filter(
        product_fk__active=True,
        product_fk_id__in=list(products_ids)
    )
    attributes_ids = set(attributes_obj.values_list('attribute_fk_id', flat=True))
    result = []

    for attribute in attributes_ids:
        attribute_lang = Attribute.objects.get(id=attribute)
        attribute_values_filtered = set(
            attributes_obj.values_list('attribute_value_fk_id', flat=True).filter(attribute_fk_id=attribute))
        result_attribute_values = list()

        for attribute_value in attribute_values_filtered:
            try:
                attribute_value_lang = AttributeValue.objects.values_list('value', flat=True).get(id=attribute_value)

            except Exception as ex:
                attribute_value_lang = ""
                ValueError(ex)
            result_attribute_values.append({'id': attribute_value,
                                            'attribute_id': attribute,
                                            'name': attribute_value_lang,
                                            'count_products': attributes_obj.filter(
                                                product_fk_id__in=filtered_products_ids, attribute_fk_id=attribute,
                                                attribute_value_fk_id=attribute_value).count(),
                                            'checked': 0,
                                            })
        result.append({
            'attribute': {'id': attribute, 'name': attribute_lang.name},
            'attribute_values': result_attribute_values
        })
    return result


def get_product_with_certain_options(product, options, user_id):
    product_obj = Product.objects.get(id=product.id)
    options_data = product_obj.options(options)
    return {'product': product_obj, 'options': options_data, 'price_data': product_obj.get_price(user_id, options)}


def get_options_of_product_objects_by_ids(product_pk, options):
    if options:
        options_obj = OptionOfProduct.objects.filter(option_fk_id__in=[id_opt['option_pk'] for id_opt in options],
                                                     product_fk_id=product_pk,
                                                     option_value_fk_id__in=[id_opt['option_val'] for id_opt in
                                                                             options]).order_by('option_fk_id')
    else:
        options_obj = OptionOfProduct.objects.none()
    return options_obj


@csrf_exempt
def get_product_price_by_options(request):
    data = json.loads(request.POST.get('data'))
    product_pk = data['product_id']
    options = data['product_options']
    options_objects = get_options_of_product_objects_by_ids(product_pk, options)
    product = Product.objects.get(id=product_pk)
    product_price = product.get_price(options=options_objects)
    res = {
        'current_price': convert_price(request, product_price['current_price']),
        'stable_price': convert_price(request, product_price['stable_price']),
        'discount': product_price['discount_value']
    }
    return JsonResponse(res, safe=False)


"""Начало нових фільтрів"""


def filtered_products(filters_json):
    _products = Product.objects.none()
    need_another_filter = True

    kwargs = {}
    if "category_id" in filters_json and filters_json['category_id'] is not None and filters_json['category_id'] != '':
        kwargs.update({'show_in_categories__id': filters_json['category_id']})
        kwargs.update({'category_fk__active': True})

    if 'filters_id' in filters_json and len(filters_json['filters_id']) > 0:
        need_another_filter = False
        kwargs.update({
            'filterofproduct__filter_fk_id__in': filters_json['filters_id'],
            'filterofproduct__filter_value_fk_id__in': filters_json['filters_values_id'],
        })

    if 'attributes_id' in filters_json and len(filters_json['attributes_id']) > 0:
        need_another_filter = False
        kwargs.update({
            'attributeofproduct__attribute_fk_id__in': filters_json['attributes_id'],
            'attributeofproduct__attribute_value_fk_id__in': filters_json['attributes_values_id'],
        })

    if 'options_id' in filters_json and len(filters_json['options_id']) > 0:
        need_another_filter = False
        kwargs.update({
            'optionofproduct__option_fk_id__in': filters_json['options_id'],
            'optionofproduct__option_value_fk_id__in': filters_json['options_values_id'],
        })
    kwargs.update({
        'calc_price__gte': Decimal(filters_json['min_price']),
        'calc_price__lte': Decimal(filters_json['max_price']),
        'active': True,
    })

    _products = Product.objects.filter(**kwargs).annotate(
        count=Concat('id', 'DISTINCT'),
    )

    if 'query' in filters_json and filters_json['query']:
        # _products = _products.filter(name__icontains=str(filters_json['query']), language=get_language())

        query = filters_json['query']
        query_split = filters_json['query'].split(' ')
        firstly = _products.filter(Q(name__istartswith=query) | Q(article__istartswith=query), active=True)
        secondly = _products.filter(Q(name__icontains=query) | Q(article__icontains=query), active=True)
        secondly_2 = _products.filter(reduce(operator.and_, [Q(name__icontains=que) for que in query_split]))
        _products = firstly.union(firstly, secondly, secondly_2)
    return _products


def attributes_in_category(category_id, checked_attributes_values):
    result = []
    if category_id is None or category_id == "":
        filters_attributes = AttributeOfProduct.objects.values('attribute_fk_id').annotate(
            attributes_values_id=Concat('attribute_value_fk_id', 'DISTINCT')
        ).all()
    else:
        filters_attributes = AttributeOfProduct.objects.values('attribute_fk_id').annotate(
            attributes_values_id=Concat('attribute_value_fk_id', 'DISTINCT')
        ).filter(
            product_fk__show_in_categories=category_id,
            # product_fk__category_fk__active=True
        )

    for filter_attribute in filters_attributes:
        # a_ - attribute; a_v_ - attribute value;
        a_id = filter_attribute['attribute_fk_id']
        a_language = Attribute.objects.values('name').get(id=a_id)
        result_a_v = list()
        for a_v_id in set(filter_attribute['attributes_values_id'].split(',')):
            a_v_language = AttributeValue.objects.values('value').get(id=a_v_id)
            result_a_v.append({
                'id': a_v_id,
                'attribute_id': a_id,
                'name': a_v_language['value'],
                'checked': 1 if int(a_v_id) in checked_attributes_values else 0,
            })
        result.append({
            'attribute': {'id': a_id, 'name': a_language['name']},
            'attribute_values': sorted(result_a_v, key=lambda val: val['name'])
        })
    return result


def filters_in_category(category_id, checked_filters_values):
    result = []
    if category_id is None or category_id == "":
        filters_filters = FilterOfProduct.objects.values('filter_fk_id').annotate(
            filters_values_id=Concat('filter_value_fk_id', 'DISTINCT')
        ).all()
    else:
        filters_filters = FilterOfProduct.objects.values('filter_fk_id').annotate(
            filters_values_id=Concat('filter_value_fk_id', 'DISTINCT')
        ).filter(
            product_fk__show_in_categories=category_id,
            # product_fk__category_fk__active=True
        )
    for filter_filter in filters_filters:
        # a_ - filter; a_v_ - filter value;
        a_id = filter_filter['filter_fk_id']
        a_language = Filter.objects.values('name').get(id=a_id)
        result_a_v = list()
        for a_v_id in set(filter_filter['filters_values_id'].split(',')):
            a_v_language = FilterValue.objects.values('value').get(id=a_v_id)
            result_a_v.append({
                'id': a_v_id,
                'filter_id': a_id,
                'name': a_v_language['value'],
                'checked': 1 if int(a_v_id) in checked_filters_values else 0,
            })
        result.append({
            'filter': {'id': a_id, 'name': a_language['name']},
            'filter_values': sorted(result_a_v, key=lambda val: val['name'])
        })
    return result


def options_in_category(category_id, checked_options_values):
    result = []
    if category_id is None or category_id == "":
        filters_options = OptionOfProduct.objects.values('option_fk_id').annotate(
            options_values_id=Concat('option_value_fk_id', 'DISTINCT')
        ).all()
    else:
        filters_options = OptionOfProduct.objects.values('option_fk_id').annotate(
            options_values_id=Concat('option_value_fk_id', 'DISTINCT')
        ).filter(
            option_fk__show_in_filters=True,
            product_fk__show_in_categories=category_id,
            # product_fk__category_fk__active=True
        )
    for filter_option in filters_options:
        # o_ - option; o_v_ - option value;
        o_id = filter_option['option_fk_id']
        o_language = Option.objects.values('name').get(id=o_id)

        result_o_v = list()
        for o_v_id in set(filter_option['options_values_id'].split(',')):
            o_v_language = OptionValue.objects.values('value').get(id=o_v_id)
            result_o_v.append({
                'id': o_v_id,
                'option_id': o_id,
                'name': o_v_language['value'],
                'checked': 1 if int(o_v_id) in checked_options_values else 0,
            })

        result.append({
            'option': {'id': o_id, 'name': o_language['name']},
            'option_values': sorted(result_o_v, key=lambda val: val['name'])
        })

    return result


"""Кінець нових фільтрів"""


@csrf_exempt
def search_product_by_query(request):
    query = request.POST.get('q')

    _products = get_all_products_in_category_or_all()
    min_price = _products.price_min
    max_price = _products.price_max
    filters_json = json.loads(request.GET.get('filter_json', "{}"))
    if 'min_price' not in filters_json:
        filters_json['min_price'] = min_price
        filters_json['max_price'] = max_price
    if 'query' not in filters_json:
        filters_json['query'] = query

    _products = filtered_products(filters_json)
    print(_products)
    tpc = len(_products)
    rest = None if tpc - PRODUCTS_SEARCH_BY_QUERY_LIMIT <= 0 else tpc - PRODUCTS_SEARCH_BY_QUERY_LIMIT
    products, paginator = get_products_field(_products, limit=PRODUCTS_SEARCH_BY_QUERY_LIMIT)

    return JsonResponse({'success': True, 'html': render_to_string('products/fast_search__list_items.html',
                                                                   {'request': request, 'products': products,
                                                                    'rest': rest})})
