import csv
import json
from time import sleep

import requests
from django.http import JsonResponse
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from apps.nova_poshta.models import Settlement
from unine_engine.globals import NP_API_URL, NP_API_KEY


# https://ukrposhta.ua/ru/dovidnik-poshtovix-adre/opis/

def update_data():
    data = {
        'apiKey': NP_API_KEY,
        'modelName': 'AddressGeneral',
        'calledMethod': 'getSettlements',
        "methodProperties": {
            "Page": "1",
        },
    }
    headers = {'Content-Type': 'application/xml'}
    response = requests.post(NP_API_URL, json=data, headers=headers)
    res = response.json()
    # try:
    #     items = [Settlement(ref=s['Ref'],
    #                         description=s['MainDescription'],
    #                         present=s['Present'],
    #                         ) for s in res['data'][0]['Addresses']]
    # except:
    #     with open('r.txt', 'a+') as f:
    #         f.write(json.dumps(res))
    # # print(d['data'])
    # Settlement.objects.all().delete()
    # objs = Settlement.objects.bulk_create(objs=items)

    # exit()
    page = 1
    all = []
    try:
        while True:
            print(page)
            response = requests.post(NP_API_URL, json=data, headers=headers)
            res = response.json()
            if len(res['data']) == 0:
                print(res)
                break
            else:
                all += res['data']
                page += 1
                data['Page'] = str(page)
                sleep(3)
                if page % 10 == 0:
                    sleep(10)

        print('ALL', len(all))
    except Exception as e:
        print(str(e))
        print('ALL', len(all))
    items = [Settlement(settlement_type=s['SettlementType'],
                        description=s['Description'],
                        region=s['Region'],
                        region_description=s['RegionsDescription'],
                        area=s['Area'],
                        area_description=s['AreaDescription']) for s in res['data']]
    objs = Settlement.objects.bulk_create(objs=items)
    # print(objs)
    # for s in res['data']:
    #     obj, is_created = Settlement.objects.update_or_create(ref=s['Ref'], defaults={
    #         'settlement_type': s['SettlementType'],
    #         'description': s['Description'],
    #         'region': s['Region'],
    #         'region_description': s['RegionsDescription'],
    #         'area': s['Area'],
    #         'area_description': s['AreaDescription'], })
    #     print(obj)
    # for r in res['data']:
    # print(r['Description'])
    pass


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
    try:
        for city in t['data'][0]['Addresses']:
            cities.append({
                'name': city['Present'],
                'ref': city['Ref'],
                'city': city['MainDescription']
            })
    except Exception as e:
        return JsonResponse({'success': False})
    return JsonResponse({'success': True, 'html': render_to_string('delivery/np_cities_list.html', {'cities': cities})})
