from django.contrib import admin

# Register your models here.
from apps.currency.models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Currency._meta.fields if field.name != "id"]
