import csv

import requests
from django.http import JsonResponse
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
# from .models import Settlement, Region
from unine_engine.globals import NP_API_URL, NP_API_KEY

# https://ukrposhta.ua/ru/dovidnik-poshtovix-adre/opis/
# def import_addresses(request):
#     file_path = f"{settings.MEDIA_ROOT}\\files\\houses.csv"
#     file = open(file_path, 'r')
#     csv_context = csv.DictReader(file, delimiter=';')
#     csv_context = list(csv_context)
#     regions = dict()
#     settlements = dict()
#     Settlement.objects.all().delete()
#     Region.objects.all().delete()
#     for obj in csv_context:
#         regions.update({obj['Область']: obj['Область']})
#         settlements.update({obj['Населений пункт'] + "_" + obj['Область']: {'Населений пункт': obj['Населений пункт'], 'Область': obj['Область']}})
#     created_regions = Region.objects.bulk_create([Region(name=region) for region in regions])
#     print('created_regions')
#
#     settlements_items = [
#         Settlement(name=settlements[settlement]['Населений пункт'], id_in_file=settlement, region_fk=Region.objects.filter(name=settlements[settlement]['Область']).first()) for
#         settlement in settlements]
#     import_steeps(Settlement, settlements_items, 1000)
#     print('created_settlements')
#     file.close()
#
#     return JsonResponse({}, safe=False)


def import_steeps(entry, items, steep=100):
    batch_size = 0
    while True:
        first = batch_size
        batch_size += steep
        next = batch_size
        del_d = items[first:next]
        if len(del_d) < 1:
            break
        entry.objects.bulk_create(del_d)
        print(first, next, len(items))


# @csrf_exempt
# def get_settlements(request):
#     q = request.POST.get('query', None)
#     print(q)
#     if q:
#         q = str(q)
#         cities = Settlement.objects.filter(name__icontains=q).values_list('name', 'region_fk__name', 'id', named=True)
#         res = []
#         for city in cities:
#             res.append({
#                 'name': f'{city.name} ({city.region_fk__name} обл.)',
#                 'id': city.id
#             })
#         print(res)
#         return JsonResponse({'success': True, 'html': render_to_string('delivery/settlements_list.html', {'settlements': res})})

@csrf_exempt
def np_get_warehouse(request):
    q = request.POST.get('query')
    ref = request.POST.get('ref')
    city = request.POST.get('city')
    data = {
        'apiKey': NP_API_KEY,
        'modelName': 'AddressGeneral',
        'calledMethod': 'getWarehouses',
        "methodProperties": {
            "CityName": city,
            "Language": "ru"
        },

        # "methodProperties": {
        #     "CityRef": ref,
        #     "CityName": q,
        # }
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(NP_API_URL, json=data, headers=headers)
    t = response.json()
    warehouses = []

    for warehouse in t['data']:
        if q.lower() in warehouse['Description'].lower():
            warehouses.append({
                'name': warehouse['Description'],
                'ref': warehouse['Ref'],
            })

    print(warehouses)
    return JsonResponse({'success': True, 'html': render_to_string('delivery/np_warehouses_list.html', {'warehouses': warehouses})})


@csrf_exempt
def np_get_cities(request):
    q = request.POST.get('query')
    data = {
        'apiKey': NP_API_KEY,
        'modelName': 'Address',
        'calledMethod': 'searchSettlements',
        "methodProperties": {
            "CityName": q,
            "Limit": 10
        }
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(NP_API_URL, json=data, headers=headers)

    t = response.json()
    cities = []
    print(t)
    try:
        for city in t['data'][0]['Addresses']:
            cities.append({
                'name': city['Present'],
                'ref': city['Ref'],
                'city': city['MainDescription']
            })
    except Exception as e:
        print(str(e))
        return JsonResponse({'success': False})
    return JsonResponse({'success': True, 'html': render_to_string('delivery/np_cities_list.html', {'cities': cities})})