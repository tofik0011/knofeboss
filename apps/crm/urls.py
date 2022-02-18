from django.urls import path, include, re_path
from apps.crm.views import *
from apps.crm.api import *

urlpatterns = [
    path('', view__crm, name="crm"),
    # path('auth/', view__auth, name="crm__view__auth"),

    path('clients/', view__clients_list, name="crm__view__clients_list"),
    path('masters/', view__masters_list, name="crm__view__masters_list"),
    path('appointments/', view__appointments_list, name="crm__view__appointments_list"),
    path('procedures/', view__procedures_list, name="crm__view__procedures_list"),
    path('order_procedure/', view__order_procedure, name="crm__view__order_procedure"),

    re_path(r'^clients/(?P<user_id>.+)/$', view__client, name='crm__view__client'),
    re_path(r'^appointments/(?P<appointment_id>.+)/$', view__appointment, name='crm__view__appointment'),
    re_path(r'^masters/(?P<user_id>.+)/$', view__master, name='crm__view__master'),
    re_path(r'^procedure/(?P<procedure_id>.+)/$', view__procedure, name='crm__view__procedure'),

    re_path(r'api/add_appointment/', add_appointment, name="api__add_appointment"),
    re_path(r'api/get_master_schedule/', get_master_day_schedule, name="api__get_master_schedule")
]
