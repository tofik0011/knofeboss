from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from easy_select2 import select2_modelform
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from tabbed_admin import TabbedModelAdmin
from .models import CartItem, Order, OrderStatus, OrderMessageTemplate


class CartItemInline(admin.TabularInline):
    # template = 'admin/edit_inline/cart_item_tabular.html'
    # form = select2_modelform(CartItem, attrs={'width': '250px'})
    fields = ('product_fk', 'option_of_product_mtm', 'qty', 'current_price')

    # can_add_related = False
    model = CartItem
    extra = 0


class OrderStatusInline(admin.TabularInline):
    model = OrderStatus
    extra = 0
    fields = ('code', 'notify_user', 'date')
    readonly_fields = ('date',)


@admin.register(OrderMessageTemplate)
class OrderMessageTemplateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderMessageTemplate._meta.fields]


@admin.register(Order)
class OrderAdmin(TabbedModelAdmin,ImportExportModelAdmin, ExportActionMixin):
    # change_form_template = 'checkout/admin_order_form.html'

    # form = select2_modelform(Order, attrs={'width': '250px'})
    list_display = ['custom_name'] + [field.name for field in Order._meta.fields if field.name not in ['id', ]]  # [field.name for field in Order._meta.fields] + ('cart_item_count')
    raw_id_fields = ('user',)
    tab_overview = (
        (None, {
            'fields': [field.name for field in Order._meta.fields if field.name not in ('date', 'id')]
        }),
    )
    tab_CartItem = (
        CartItemInline,
    )
    tab_OrderStatus = (
        OrderStatusInline,
    )
    tabs = [
        (_('admin__general'), tab_overview),
        (_('admin__products'), tab_CartItem),
        (_('admin__order_statuses'), tab_OrderStatus),
    ]
    class OrderResource(resources.ModelResource):
        class Meta:
            model = Order
            fields = ('first_name''last_name',)


    resource_class = OrderResource

    def custom_name(self, instance):
        return f'{_("checkout__order")} #{instance.id}'

    # def first_name_ll(self, instance):
    #     # assuming get_full_address() returns a list of strings
    #     # for each line of the address and you want to separate each
    #     # line by a linebreak
    #     return format_html_join(
    #         mark_safe('<br> test test'),
    #         '{}',
    #         ((line,) for line in instance.first_name),
    #     ) or mark_safe("<span class='errors'>I can't determine this address.</span>")

    # @staticmethod
    # def cart_item_count(obj):
    #     return obj.cartitem_set.count()

    # def response_change(self, request, obj):
    #     if "_make-unique" in request.POST:
    #         obj.total = Decimal(23)
    #         obj.save()
    #         self.message_user(request, "This villain is now unique")
    #         return HttpResponseRedirect(".")
    #     return super(self).response_change(request, obj)

    # def get_urls(self):
    #     urls = super().get_urls()
    #     my_urls = [
    #         path('immortal/', self.set_immortal),
    #     ]
    #     return my_urls + urls
    #
    # def set_immortal(self, request):
    #     print(self.model.objects.all().update(total=Decimal(600)))
    #     self.message_user(request, "NewPrice " + str(Decimal(600)))
    #     return HttpResponseRedirect("../")

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Cart._meta.fields]


# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in CartItem._meta.fields]
