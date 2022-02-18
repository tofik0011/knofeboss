from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.banner.models import Banner
from django.utils.translation import ugettext_lazy as _
from unine_engine import settings


@admin.register(Banner)
class BannerAdmin(TabbedTranslationAdmin):
    list_display = ['keyword', 'active', 'image']
    list_editable = ['active', 'image']
    list_display_links = ('keyword',)
    sortable = 'order'
    search_fields = ['name', ]
    fieldsets = [
        (None, {'fields': (
            'keyword',

            'image', 'content_text',  'button_link',
        )}),
    ]

    class Meta:
        model = Banner

    class Media:
        js = ('admin/admin_languages.js',)
        css = {'screen': ('admin/admin_languages.css',), }
