from django.contrib import admin
from .models import Redirects


@admin.register(Redirects)
class AdminRedirects(admin.ModelAdmin):
    list_display = [field.name for field in Redirects._meta.fields]
    list_editable = [field.name for field in Redirects._meta.fields if field.name != "id"]