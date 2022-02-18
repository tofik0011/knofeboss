from django.urls import path
from .api import np_get_warehouse, np_get_cities

urlpatterns = [
    # path('import_addresses/', import_addresses, name='import_addresses'),
    # path('api/delivery/get_settlements', get_settlements, name='delivery__get_settlements'),
    path('api/np_get_cities/', np_get_cities, name="np_get_cities"),
    path('api/np_get_warehouses/', np_get_warehouse, name="np_get_warehouses"),
]
