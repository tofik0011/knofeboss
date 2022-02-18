from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin
from tabbed_admin import TabbedModelAdmin
from django.utils.translation import ugettext_lazy as _, get_language
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import MenuItem, MenuItemTOP
from unine_engine.globals import LANGUAGES


@admin.register(MenuItem)
class MenuItemAdmin(DraggableMPTTAdmin, TabbedTranslationAdmin):
    mptt_level_indent = 20
    mptt_indent_field = "parent"
    list_display = ['tree_actions', 'something', 'order', 'parent', ]
    list_editable = ('parent', 'order')
    list_display_links = ('something', )
    sortable = ['menu_keyword', 'order']
    model = MenuItem

    def something(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance,  # Or whatever you want to put here
        )

    something.short_description = 'something nice'


@admin.register(MenuItemTOP)
class MenuItemTOPTopAdmin(DraggableMPTTAdmin, TabbedTranslationAdmin):
    mptt_level_indent = 20
    mptt_indent_field = "parent"
    list_display = ['tree_actions', 'something', 'order', 'parent', ]
    list_editable = ('parent', 'order')
    list_display_links = ('something', )
    sortable = ['menu_keyword', 'order']
    model = MenuItemTOP

    def something(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance,  # Or whatever you want to put here
        )

    something.short_description = 'something nice'
