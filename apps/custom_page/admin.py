from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin
from mptt.admin import MPTTModelAdmin
from tabbed_admin import TabbedModelAdmin

from unine_engine import globals
from .models import CustomPage


@admin.register(CustomPage)
class CustomPageAdmin(MPTTModelAdmin, TabbedTranslationAdmin):
    mptt_level_indent = 20
    list_display = ['id', 'name_admin', 'active', 'link', ]
    list_editable = ['active', ]
    list_display_links = ('id', 'name_admin',)
    sortable = 'order'
    search_fields = ['name', ]
    fieldsets = [
        ('Стандарт', {'fields': ('parent', 'active', ('name', 'description'))}),
        ('SEO', {'fields': ('link', 'seo_title', 'seo_description')}),
    ]

    class Meta:
        model = CustomPage

    class Media:
        js = ('admin/admin_languages.js',)
        css = {'screen': ('admin/admin_languages.css',), }

    def name_admin(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.__str__(),
        )

    name_admin.short_description = _("admin__name")
