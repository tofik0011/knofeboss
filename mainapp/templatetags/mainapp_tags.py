from __future__ import unicode_literals
import re
from itertools import groupby

from django import template
import os.path

from django.db.models import Count
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext as _, get_language
from apps.products.models import Category, Product
from apps.custom_page.models import CustomPage
from unine_engine.settings import MEDIA_ROOT, BASE_DIR
from ..get_data import render_menu, get_settings
from apps.checkout.get_data import get_cart, render_cart_items
from apps.blog.models import Article, Category as A_Category
from mainapp.models import Settings, TextContent, SeoData
from apps.menu.models import MenuItem, MenuItemTOP
import json

register = template.Library()


@register.simple_tag
def call_method(obj, method_name, **kwargs):
    """
    Визиває функцію моделі з параметрами
    Example {% call_method article 'get_last_articles' limit=10 as articles %}
    :param obj: Модель
    :param method_name: Функція
    :param kwargs: Параметри
    :return: Результат функції
    """
    method = getattr(obj, method_name)
    return method(**kwargs)


@register.simple_tag
def get_svg(url):
    try:
        f = open(os.path.join(MEDIA_ROOT, url))
        content = f.read()
        return content
    except Exception as e:
        return ''


@register.filter
def filter_image_x2(value, x=2):
    """Фільтер для збільшеня width/height картинки в 2 рази"""
    return int(value) * x


@register.simple_tag
def tag_breadcrumbs(request):
    breadcrumbs = []
    url = request.path
    urls = url.split('/')
    urls = [var for var in urls if var]
    for link in urls:
        if link == 'checkout':
            breadcrumbs.append({'title': _('checkout'), 'link': reverse('view__checkout')})
            continue
        if link == 'search':
            breadcrumbs.append({'title': _('products__search'), 'link': reverse('view__search')})
            continue
        if link == 'blog':
            breadcrumbs.append({'title': _('blog'), 'link': reverse('blog')})
            continue
        # if link == 'registration':
        #     breadcrumbs.append({'title': _('account__registration'), 'link': reverse('view__registration')})
        #     continue
        # if link == 'login':
        #     breadcrumbs.append({'title': _('account__login'), 'link': reverse('view__login')})
        #     continue
        if link == 'password_reset':
            breadcrumbs.append({'title': _('account__password_reset'), 'link': reverse('view__password_reset')})
            continue
        if link == 'account':
            breadcrumbs.append({'title': _('account'), 'link': reverse('view__account')})
            continue
        if link == 'contacts':
            breadcrumbs.append({'title': _('contacts'), 'link': reverse('view__contacts')})
            continue
        if link == 'catalog':
            breadcrumbs.append({'title': _('products__catalog'), 'link': reverse('catalog')})
            continue
        if link == 'specials':
            breadcrumbs.append({'title': _('specials'), 'link': reverse('specials')})
            continue

        """Категорії товарів"""
        try:
            category = Category.get_category_by_link(link)
            breadcrumbs.append({'title': category.name, 'link': category.get_absolute_url()})
            continue
        except Exception as error:
            pass

        """Товари"""
        try:
            product = Product.get_product_by_link(link)
            breadcrumbs.append({'title': product.name, 'link': product.get_absolute_url()})
            continue
        except Exception as error:
            pass

        """Категорії статей"""
        try:
            category = A_Category.get_category_by_url(link)
            breadcrumbs.append({'title': category.name, 'link': category.get_absolute_url()})
            continue
        except Exception as error:
            pass

        """Статті"""
        try:
            article = Article.get_article_by_url(link)
            breadcrumbs.append({'title': article.name, 'link': article.get_absolute_url()})
            continue
        except Exception as error:
            pass

        """Кастомні сторінки"""
        try:
            custom_page = CustomPage.get_custompage_by_url(link)
            breadcrumbs.append({'title': custom_page.name, 'link': custom_page.get_absolute_url()})
            continue
        except Exception as error:
            pass
    return breadcrumbs


@register.simple_tag
def tag_get_full_path(request, path=None):
    if path:
        url = 'https://' + request.get_host() + path if request.is_secure() else 'http://' + request.get_host() + path
    else:
        url = 'https://' + request.get_host() + request.path if request.is_secure() else 'http://' + request.get_host() + request.path
    return url


@register.simple_tag
def tag_get_text_content(keyword):
    text_content = TextContent.objects.filter(keyword=keyword).first()
    return text_content


@register.simple_tag
def tag_get_seo_data(keyword):
    seo_data = SeoData.objects.filter(keyword=keyword).first()
    return seo_data


@register.simple_tag
def tag_get_favicon():
    s = get_settings()
    return s.favicon


@register.simple_tag
def tag_get_sitename():
    s = get_settings()
    return s.name


@register.simple_tag
def tag_get_google_analytics():
    return get_settings().google_analytics_code


@register.filter
def filter_phone_trim(phone):
    phone = re.sub("\D+", '', str(phone))
    return str(phone)


@register.simple_tag
def tag_get_menu():
    top = MenuItemTOP.objects.filter( active=True)
    main = MenuItem.objects.filter( active=True)
    # bottom = MenuItem.objects.filter(menu_keyword='bottom', active=True)
    return {'top': top, 'main': main}

@register.filter
def media_url(value, request):
    return ''.join([request.scheme, "://", request.META['HTTP_HOST'], value])

@register.filter
def add_language_to_link(url, lng):
    url = url.split('/')
    url[2] = f"{url[2]}/{lng}"
    return '/'.join(url)
