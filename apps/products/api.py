import json
import random
import string
from decimal import Decimal

from django.core.paginator import Paginator
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from filebrowser.base import FileObject

from unine_engine.globals import PRODUCTS_PER_PAGE, PRODUCTS_SORTING, REVIEWS_PER_PAGE, LANGUAGES
from apps.products.get_data import get_attributes_list_of_products, get_all_products_in_category_and_filter_attributes, \
    get_products_field, filtered_products, attributes_in_category, filters_in_category, options_in_category
from apps.products.models import AttributeValue, FilterValue, OptionValue, Review, Product, OptionOfProduct, AttributeOfProduct, Option, Attribute

def get_attribute_values_id_by_attribute_id_json(request):
    # Використовується в адмінці
    attribute_id = request.GET.get("attribute_id")
    result = []
    if attribute_id:
        attributes_values = AttributeValue.objects.filter(attribute_fk=attribute_id)
        for attribute_value in attributes_values:
            result.append({'id': attribute_value.pk, 'name': attribute_value.__str__()})
    return JsonResponse(result, safe=False)


def get_filter_values_id_by_filter_id_json(request):
    filter_id = request.GET.get("filter_id")
    result = []
    if filter_id:
        filters_values = FilterValue.objects.filter(filter_fk=filter_id)
        for filter_value in filters_values:
            result.append({'id': filter_value.pk, 'name': filter_value.__str__()})
    return JsonResponse(result, safe=False)


def get_option_values_id_by_option_id_json(request):
    option_id = request.GET.get("option_id")
    result = []
    if option_id:
        options_values = OptionValue.objects.filter(option_fk=option_id)
        for option_value in options_values:
            result.append({'id': option_value.pk, 'name': option_value.__str__()})
    return JsonResponse(result, safe=False)


@csrf_exempt
def get_template_product_cart(request):
    product = Product.objects.get(id=request.POST.get('product_id'))
    if request.POST.get('product_id'):
        return HttpResponse(render_to_string('products/product_min.html', {'product': product}, request))
    else:
        raise Http404('Product Not Fount')


@csrf_exempt
def get_template_products_cart(request):
    if request.POST.get('products_id[]'):
        products_id = request.POST.getlist('products_id[]')
        sorting = request.POST.get('sorting')
        page = request.POST.get('page', 1)
        products_field, products_paginator = get_products_field(products_id, page=page, sorting=sorting)
        # return render(request, 'products/product_min.html', {'product': get_product_field(request.POST.get('product_id'))})
        data = render_to_string('products/category_content_products.html', {'products': products_field, 'products_paginator': products_paginator}, request)
        return HttpResponse(data)
    else:
        raise Http404('Product Not Fount')


@csrf_exempt
def get_template_catalog(request):
    if request.method != 'POST':
        JsonResponse({}, safe=False)
    import time
    start_time = time.time()  # TIMER TIMER TIMER TIMER TIMER TIMER
    filters_json = json.loads(request.body.decode('utf-8'))
    products = filtered_products(filters_json)
    page = filters_json['page'] if 'page' in filters_json else 1
    sorting = filters_json['sorting'] if 'sorting' in filters_json else PRODUCTS_SORTING[0][0]
    category_id = filters_json['category_id'] if 'category_id' in filters_json else None
    print("--- %s 1 seconds ---" % (time.time() - start_time))  # TIMER TIMER TIMER TIMER TIMER TIMER
    attributes = attributes_in_category(category_id, filters_json['attributes_values_id'] if 'attributes_values_id' in filters_json else [])
    filters = filters_in_category(category_id, filters_json['filters_values_id'] if 'filters_values_id' in filters_json else [])
    options = options_in_category(category_id, filters_json['options_values_id'] if 'options_values_id' in filters_json else [])

    if len(products) < PRODUCTS_PER_PAGE * int(page) - PRODUCTS_PER_PAGE:
        page = 1
    temp_products_paginator = None
    print("--- %s 2 seconds ---" % (time.time() - start_time))  # TIMER TIMER TIMER TIMER TIMER TIMER
    if type(page) != int and len(page.split(',')) > 0:
        page_array = page.split(',')
        products, _products_paginator = get_products_field(products, limit=PRODUCTS_PER_PAGE, sorting=sorting, page=page_array[0], with_options=True)
        for index, page in enumerate(page_array):
            if index == 0:
                continue
            temp_products, temp_products_paginator = get_products_field(products, limit=PRODUCTS_PER_PAGE, sorting=sorting, page=page, with_options=True)
            products.extend(temp_products)
    else:
        products, _products_paginator = get_products_field(products, limit=PRODUCTS_PER_PAGE, sorting=sorting, page=page, with_options=True)
    print("--- %s 3 seconds ---" % (time.time() - start_time))  # TIMER TIMER TIMER TIMER TIMER TIMER
    template_products = render_to_string('products/category_content_products.html',{
        'products': products, 'products_paginator': temp_products_paginator if temp_products_paginator else _products_paginator
    }, request)
    template_chips = render_to_string('products/category_parts/badges.html', {
        "category_attributes": attributes,
        "category_filters": filters,
        "category_options": options,
    })
    print("--- %s 4 seconds ---" % (time.time() - start_time))  # TIMER TIMER TIMER TIMER TIMER TIMER
    return JsonResponse({'products_template': template_products, 'chips_template': template_chips}, safe=False)


@csrf_exempt
def add_review(request):
    try:
        _name = request.POST.get('author', None)
        _text = request.POST.get('text', None)
        _product_id = request.POST.get('product_id', None)
        _rating = int(request.POST.get('rating', None))
        if len(_name) < 1 or len(_text) < 1:
            return JsonResponse({'success': False, 'error': _('error__incorrect_form')})
        Review.objects.create(name=_name, text=_text, rating=_rating, is_approved=False, product_fk_id=_product_id)
        return JsonResponse({'success': True})
    except Exception as e:
        print(str(e))
        return JsonResponse({'success': False})


@csrf_exempt
def load_more_reviews(request):
    _product_id = request.POST.get('product_id', None)
    _page = request.POST.get('page', None)

    reviews = Review.objects.filter(product_fk_id=_product_id, is_approved=True).values('name', 'text', 'rating', 'added_date').order_by('-added_date')
    paginator = Paginator(reviews, REVIEWS_PER_PAGE).page(int(_page))
    next = -1
    if paginator.has_next():
        next = paginator.next_page_number()
    print(next)
    return JsonResponse({'success': True, 'next_page': next, 'html': render_to_string('products/reviews_list.html', {'reviews': paginator})})
