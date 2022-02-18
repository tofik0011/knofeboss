from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin
from tabbed_admin import TabbedModelAdmin
from django.utils.translation import ugettext_lazy as _, get_language
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Settings, TextContent, SeoData, GoogleMap
from mptt.admin import MPTTModelAdmin

from unine_engine.globals import LANGUAGES


@admin.register(Settings)
class SettingsAdmin(TabbedTranslationAdmin):
    list_display = ['admin_name']

    def admin_name(self, instance):
        return _('admin__settings')


@admin.register(SeoData)
class SeoDataAdmin(TabbedTranslationAdmin):
    list_display = [field.name for field in SeoData._meta.fields]
    list_editable = [field.name for field in SeoData._meta.fields if field.name != "id"]


@admin.register(TextContent)
class TextContentAdmin(TabbedTranslationAdmin):
    list_display = [field.name for field in TextContent._meta.fields]
    list_editable = [field.name for field in TextContent._meta.fields if field.name != "id"]

@admin.register(GoogleMap)
class GoogleMapAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GoogleMap._meta.fields if field.name != "id"]
