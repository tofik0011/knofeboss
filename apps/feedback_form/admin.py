from django.contrib import admin

from apps.feedback_form.models import FormRequest


@admin.register(FormRequest)
class FormRequest(admin.ModelAdmin):
    list_display = [field.name for field in FormRequest._meta.fields if field.name != "id"]