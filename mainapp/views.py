from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt

from apps.contacts.models import Phone, Email, Address
from apps.products.models import Category
from mainapp.get_data import get_settings
from mainapp.models import Settings, GoogleMap


def get_robots_txt(request):
    data = Settings.objects.values_list('robots_txt', flat=True).first()
    return HttpResponse(data, content_type='text/plain')


def get_sitemap(request):
    settings = get_settings()
    file = open(settings.sitemap.path_full, mode='r', encoding="utf-8")
    res = file.read()
    return HttpResponse(res, content_type="application/xml")


# TODO view__
def get_index_page(request, keyword='index'):
    category_all_mainpage = Category.objects.all()
    category_mainpage = category_all_mainpage.filter(active_in_mainpage=True)
    """Универсальная функция для реквеста на страницу"""
    return render(request, "mainapp/pages/index.html", {"category_mainpage":category_mainpage,})


def get_contacts_page(request):
    data = {}
    # for k in CONTACTS_KEYWORDS:
    #     data.update({k[0]: {
    #         'phones': Phone.objects.filter(keyword=k[0]).values_list('phone', flat=True),
    #         'emails': Email.objects.filter(keyword=k[0]).values_list('email', flat=True),
    #         'address': AddressLanguage.objects.filter(address_fk__keyword=k[0], language=get_language()).values_list('address', flat=True),
    #     }})
    return render(request, "mainapp/pages/contacts.html", {'data': data, })


@csrf_exempt
def api_google_map(request):
    markers = GoogleMap.objects.all()
    result = [{'name_marker': marker.name_marker, 'lat': marker.lat, 'longitude': marker.longitude, } for marker in markers]
    return JsonResponse({'success': True, 'data': result, })


def view__production(request):
    return render(request, "mainapp/pages/production.html")


def igreen(request):
    return render(request, "footer_igreen.html")


def igreen_b(request):
    return render(request, "footer_igreen_bisnes.html")
