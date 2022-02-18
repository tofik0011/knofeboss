from django.urls import path
from .api import np_get_warehouse, np_get_cities, update_data

urlpatterns = [
    path('api/np_get_cities/', np_get_cities, name="np_get_cities"),
    path('api/nova_poshta_update_data/', update_data, name="np_update_data"),
    path('api/np_get_warehouses/', np_get_warehouse, name="np_get_warehouses"),
]
