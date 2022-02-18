from django.urls import path, include

from apps.currency.views import currency_set

urlpatterns = [
    path('currency_set/', currency_set, name="currency_set"),
]
