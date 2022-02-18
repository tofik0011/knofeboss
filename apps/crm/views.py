from decimal import Decimal, ROUND_CEILING
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import get_language
from apps.crm.models import Client, ExtendedUser, Master, Procedure
from apps.currency.models import Currency
from unine_engine import globals


def add_user():
    user, created_user = ExtendedUser.objects.get_or_create(username='master2',
                                                            defaults={
                                                                'first_name': 'master2',
                                                                'last_name': 'master2',
                                                                'email': 'admin@gmail.com',
                                                                'phone': '12412351235',
                                                            })

    exuser = ExtendedUser.objects.get(id=user.id)
    exuser.master = Master.objects.create(user_fk_id=user.id)
    exuser.set_password('qweqwe123123')
    exuser.save()


def view__crm(request):
    return render(request, 'crm/index.html')


def view__clients_list(request):
    clients = Client.objects.all()
    return render(request, 'crm/account/clients.html', {'clients': clients})


def view__appointments_list(request):
    pass


def view__procedures_list(request):
    procedures = Procedure.objects.all()
    for p in procedures:
        p.l = p.procedurelanguage_set.filter(language=get_language()).first()
        print(p.l)
    return render(request, 'crm/account/procedures.html', {'procedures': procedures})


def view__masters_list(request):
    masters = Master.objects.all()
    return render(request, 'crm/account/masters.html', {'masters': masters})


def view__client(request, user_id):
    client = Client.objects.get(user_fk_id=user_id)
    return render(request, 'crm/account/client_detail.html', {'clients': client})


def view__order_procedure(request):
    procedure_id = request.GET.get('procedure_id', None)
    res = {
        'procedures': Procedure.objects.all(),
        'choosed_procedure_id': int(procedure_id),
        'masters': Master.objects.all(),
    }
    return render(request, 'crm/account/order_procedure.html', res)


def view__master(request):
    pass


def view__appointment(request):
    pass


def view__procedure(request, procedure_id):
    procedure = Procedure.objects.get(id=procedure_id)
    return render(request, 'crm/account/procedure_detail.html', {'p': procedure})
