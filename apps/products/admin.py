from django.contrib import admin
from django.forms import TextInput, Textarea
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from mptt.querysets import TreeQuerySet
from tabbed_admin import TabbedModelAdmin
from easy_select2 import select2_modelform, apply_select2

from .admin_actions import action_copy_category, action_copy_product
from .models import *


class AttributeOfProductInline(admin.TabularInline):
    model = AttributeOfProduct
    extra = 0
    # autocomplete_fields = ['attribute_value_fk', 'attribute_fk']
    verbose_name = _('admin__attributes')


class FilterOfProductInline(admin.TabularInline):
    model = FilterOfProduct
    extra = 0
    # autocomplete_fields = ['filter_value_fk', 'filter_fk']
    verbose_name = _('admin__filters')


class OptionOfProductInline(admin.TabularInline):
    model = OptionOfProduct
    extra = 0
    # autocomplete_fields = ['option_value_fk', 'option_fk']
    # form = select2_modelform(OptionOfProduct, attrs={'width': '250px'})
    verbose_name = _('admin__options')


class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 0
    max_num = 1
    verbose_name = _('admin__discount')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    verbose_name = _('admin__images')


# @admin.register(AttributeOfProduct)
# class AttributeOfProductAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in AttributeOfProduct._meta.fields]
#     list_editable = [field.name for field in AttributeOfProduct._meta.fields if field.name != "id"]


# @admin.register(OptionOfProduct)
class OptionOfProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OptionOfProduct._meta.fields]
    list_editable = [field.name for field in OptionOfProduct._meta.fields if field.name != "id"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_editable = [field.name for field in Review._meta.fields if field.name not in ['id', 'added_date']]
    list_display = [field.name for field in Review._meta.fields if field.name]
    autocomplete_fields = ('product_fk',)
    search_fields = ['product_fk']
    # prepopulated_fields = {"product_fk": ("title",)}
    # radio_fields = {"product_fk": admin.HORIZONTAL}


@admin.register(Unit)
class UnitAdmin(TabbedTranslationAdmin):
    list_display = ['min_amount', 'symbol', 'name']

    # prepopulated_fields = {"product_fk": ("title",)}
    # radio_fields = {"product_fk": admin.HORIZONTAL}
    class Media:
        js = ('admin/admin_languages.js',)
        css = {'screen': ('admin/admin_languages.css',), }


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin, MPTTModelAdmin, TabbedTranslationAdmin):
    actions = [action_copy_category, ]
    mptt_level_indent = 20
    list_display = ['id', 'name_admin', 'active', 'link', 'image','active_in_mainpage']
    list_editable = ['active','active_in_mainpage' ]
    list_display_links = ('id', 'name_admin',)
    sortable = 'order'
    search_fields = ['name', ]
    fieldsets = [
        ('Стандарт', {'fields': ('image', 'active_in_mainpage', 'image_banner', 'parent', 'active')}),
        ('Описание', {'fields': ('name', 'h1', 'description')}),
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


@admin.register(Product)
class ProductAdmin(TabbedTranslationAdmin):
    list_filter = ()
    list_per_page = 15
    actions = [action_copy_product, ]
    inlines = [AttributeOfProductInline, OptionOfProductInline, FilterOfProductInline, DiscountInline, ProductImageInline]
    list_display = ['id', 'name', 'category_fk', 'price', 'active']
    # list_editable = [field.name for field in Product._meta.fields if field.name not in ('id_1c', 'lowest_option_price', 'calc_price', 'id', 'added_date', 'update_date')]
    list_editable = ['active', 'category_fk']
    search_fields = ('article', 'id_import', 'name')
    autocomplete_fields = ['show_in_categories', 'category_fk', 'similar']
    fieldsets = [
        ('Стандарт', {
            'fields':
                (
                    'id_import', 'article', 'is_bestseller', 'unit', 'image', 'active',
                    'price', 'qty', 'category_fk', 'show_in_categories', 'similar'
                )
        }),
        ('Описание', {'fields': ('name', 'description')}),
        ('SEO', {'fields': ('link', 'seo_title', 'seo_description')}),
    ]

    def save_model(self, request, obj, form, change):
        try:
            # if not obj.show_in_categories.filter(id=obj.category_fk.id).exists():
            # obj.show_in_categories.set([c.id for c in list(obj.category_fk.get_ancestors(include_self=True))])
            if len(form.cleaned_data['show_in_categories']) == 0 and obj.category_fk:
                form.cleaned_data['show_in_categories'] = [obj.category_fk]
        except Exception as ex:
            print(ex)
        super(ProductAdmin, self).save_model(request, obj, form, change)

    class Meta:
        model = Product

    class Media:
        js = ('admin/admin_languages.js',)
        css = {'screen': ('admin/admin_languages.css',), }


# @admin.register(Discount)
# class DiscountAdmin(admin.ModelAdmin):
#     # change_form_template = 'admin_custom/product.html'
#     list_display = [field.name for field in Discount._meta.fields if field.name != "id"]


@admin.register(Attribute)
class AttributeAdmin(TabbedTranslationAdmin):
    list_display = ['name', 'id_1c', 'keyword', 'show_in_filters', ]
    fields = ['keyword', 'id_1c', 'show_in_filters', 'name', ]
    search_fields = ['id_1c', 'keyword', 'name', ]

    class Media:
        js = ('admin/admin_languages.js',)
        css = {'screen': ('admin/admin_languages.css',), }


@admin.register(AttributeValue)
class AttributeValueAdmin(TabbedTranslationAdmin):
    list_display = ['value', 'id_1c', 'attribute_fk', ]
    fields = ['id_1c', 'attribute_fk', 'value', ]
    search_fields = ['value', 'id_1c', ]
    autocomplete_fields = ['attribute_fk', ]

    class Media:
        js = ('admin/admin_languages.js',)
        css = {'screen': ('admin/admin_languages.css',), }


@admin.register(Filter)
class FilterAdmin(TabbedTranslationAdmin):
    list_display = ['name', ]
    fields = ['name', ]
    search_fields = ['name', ]

    class Media:
        js = ('admin/admin_languages.js',)
        css = {'screen': ('admin/admin_languages.css',), }


@admin.register(FilterValue)
class FilterValueAdmin(TabbedTranslationAdmin):
    list_display = ['value', 'filter_fk', ]
    fields = ['filter_fk', 'value', ]
    search_fields = ['filter_fk', 'value', ]

    class Media:
        js = ('admin/admin_languages.js',)
        css = {'screen': ('admin/admin_languages.css',), }


@admin.register(Option)
class OptionAdmin(TabbedTranslationAdmin):
    list_display = ['keyword', 'operation', 'required', 'show_in_filters', 'name']
    fields = ['keyword', 'operation', 'required', 'show_in_filters', 'name']
    search_fields = ['name', 'keyword']

    class Media:
        js = ('admin/admin_languages.js',)
        css = {'screen': ('admin/admin_languages.css',), }


@admin.register(OptionValue)
class OptionValueAdmin(TabbedTranslationAdmin):
    list_display = ['value', 'id_1c', 'option_fk']
    fields = ['option_fk', 'id_1c', 'value']
    autocomplete_fields = ['option_fk', ]
    search_fields = ['value', ]

    class Media:
        js = ('admin/admin_languages.js',)
        css = {'screen': ('admin/admin_languages.css',), }
