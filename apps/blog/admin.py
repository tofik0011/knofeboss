from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin
from mptt.admin import MPTTModelAdmin
from .admin_actions import action_copy_article
from .models import Article, Category


@admin.register(Article)
class ArticleAdmin(TabbedTranslationAdmin):
    actions = [action_copy_article, ]
    group_fieldsets = True
    list_display = ['name', 'active', 'link', 'image']
    list_editable = ['active', ]
    fieldsets = [
        ('Стандарт', {'fields': ('image', ('category_fk', 'show_in_categories'), 'active')}),
        ('Описание', {'fields': ('link', 'name', 'short_description', 'description')}),
        ('SEO', {'fields': ('seo_title', 'seo_description')}),
    ]

    class Meta:
        model = Article

    class Media:
        js = ('admin/admin_languages.js',)
        css = {'screen': ('admin/admin_languages.css',), }


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin, TabbedTranslationAdmin):
    mptt_level_indent = 20
    list_display = ['name_admin', 'active', 'link', 'image']
    list_editable = ['active', ]
    list_display_links = ('name_admin',)
    sortable = 'order'
    fieldsets = [
        ('Стандарт', {'fields': ('image', 'parent', 'active')}),
        ('Описание', {'fields': ('name', 'description')}),
        ('SEO', {'fields': ('link', 'seo_title', 'seo_description')}),
    ]

    def name_admin(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.__str__(),
        )

    name_admin.short_description = "Назва"

    class Media:
        js = ('admin/admin_languages.js',)
        css = {'screen': ('admin/admin_languages.css',), }
