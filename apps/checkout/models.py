import json
import threading
from datetime import datetime
from decimal import Decimal

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _, get_language
from smart_selects.db_fields import ChainedManyToManyField


from apps.contacts.models import Email
from apps.currency.views import get_currency_data_for_order, convert_price
from apps.email_notifications.views import send_html_mail
from django_currentuser.middleware import get_request, get_current_user
from mainapp.helper import validate_phone, validate_email, trim_phone
from unine_engine.globals import ORDER_STATUS_CHOICES, DELIVERY_CHOICES, PAYMENT_CHOICES
from apps.products.models import Product, OptionOfProduct, Discount


class Order(models.Model):
    user = models.ForeignKey('profile.Profile', verbose_name=_('admin__user'), on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(verbose_name=_("admin__first_name"), max_length=255, blank=True)
    last_name = models.CharField(verbose_name=_("admin__last_name"), max_length=255, blank=True)
    phone = models.CharField(verbose_name=_("admin__phone"), max_length=20, blank=True)
    delivery_settlement = models.CharField(verbose_name=_("admin__delivery_settlement"), max_length=255, blank=True, null=True)
    delivery_address = models.CharField(verbose_name=_("admin__delivery_address"), max_length=255, blank=True, null=True)
    post_index = models.CharField(verbose_name=_("admin__post_index"), max_length=255, blank=True, null=True)
    email = models.EmailField(verbose_name=_("admin__email"), max_length=255, blank=True)
    delivery_type = models.CharField(verbose_name=_("admin__delivery_type"), choices=DELIVERY_CHOICES, max_length=255)
    payment_type = models.CharField(verbose_name=_("admin__payment_type"), choices=PAYMENT_CHOICES, max_length=255)
    comment = models.TextField(verbose_name=_("admin__comment"), blank=True)
    date = models.DateTimeField(verbose_name=_("admin__date"), auto_now_add=True)
    currency_data = models.TextField(verbose_name=_("admin__currency_data"), blank=True)
    is_paid = models.BooleanField(verbose_name=_("admin__is_paid"), default=False)
    is_one_click_order = models.BooleanField(verbose_name=_("admin__is_one_click_order"), default=False)
    total = models.DecimalField(verbose_name=_("admin__total"), max_digits=9, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = _("admin_order_model")
        verbose_name_plural = _("admin_orders_model")

    def __str__(self):
        return str("Заказ" + ' №{0}'.format(str(self.id)))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, add_order_status=False):
        super(Order, self).save()
        if add_order_status:
            OrderStatus.objects.create(code=ORDER_STATUS_CHOICES[0][0], order_fk_id=self.id)

    @property
    def full_delivery_address(self):
        if self.delivery_type == 'pickup':
            return ''
        else:
            return f'{self.delivery_settlement}, {self.delivery_address} {self.post_index if self.post_index else ""}'

    @property
    def current_status(self):
        return OrderStatus.objects.filter(order_fk_id=self.id).order_by('date').last()

    @property
    def statuses_list(self):
        return OrderStatus.objects.filter(order_fk_id=self.id).order_by('date')

    @property
    def order_items(self):
        return self.cartitem_set.all()

    @property
    def get_currency_data(self):
        cd = self.currency_data.replace("'", '"')
        return json.loads(cd)

    def get_total_price(self):
        order_items = self.cartitem_set.all()
        total_price = order_items.aggregate(Sum('current_price'))
        return total_price['current_price__sum']

    @staticmethod
    def validate_order_form(d):
        errors = []
        first_name = d.get('first_name', None)
        last_name = d.get('last_name', None)
        email = d.get('email', None)
        phone = trim_phone(d.get('phone', None))

        delivery_type = d.get('delivery_type', None)

        delivery_obl = d.get('delivery_obl', None)
        delivery_settlement = d.get('delivery_settlement', None)
        delivery_street = d.get('delivery_street', None)
        delivery_house = d.get('delivery_house', None)

        post_index = d.get('post_index', None)

        payment_type = d.get('payment_type', None)
        privacy_policy = d.get('privacy_policy', None)
        comment = d.get('comment', None)

        if not first_name:
            errors.append({'#first_name': _('error__required_field')})
        if not last_name:
            errors.append({'#last_name': _('error__required_field')})

        if not phone:
            errors.append({'#phone': _('error__required_field')})
        elif not validate_phone(phone):
            errors.append({'#phone': _('error__invalid_phone')})

        if not email:
            errors.append({'#email': _('error__required_field')})
        elif not validate_email(email):
            errors.append({'#email': _('error__invalid_email')})

        if delivery_type == 'pickup':
            pass
        elif delivery_type == 'new_post':
            if not delivery_settlement:
                errors.append({'#np_settlement_input': _('empty_field')})
            if not delivery_street:
                errors.append({'#np_warehouse_input': _('empty_field')})
        elif delivery_type in ('delivery', 'courier', 'in_time', 'avtoluks', 'ukr_post'):
            if not delivery_obl:
                errors.append({'#custom_obl_input': _('empty_field')})
            if not delivery_settlement:
                errors.append({'#custom_settlement_input': _('empty_field')})
            if not delivery_street:
                errors.append({'#custom_street_input': _('empty_field')})
            if not delivery_house:
                errors.append({'#custom_house_input': _('empty_field')})
        else:
            errors.append({'#delivery_type': _('error__required_field')})

        if not payment_type or payment_type not in dict(PAYMENT_CHOICES).keys():
            errors.append({'#payment_type': _('error__required_field')})

        if not privacy_policy:
            errors.append({'#payment_type': _('error__required_field')})

        from apps.checkout.get_data import get_cart
        user = get_current_user()
        request = get_request()
        cart = get_cart(request)
        if user.is_authenticated:
            if user.type_profile_fk.min_price > cart.total_price:
                errors.append({'#checkout_submit': f"{_('error__min_price_delivery')}: {convert_price(request, user.type_profile_fk.min_price)}"})

        if len(errors) > 0:
            return {'success': False, 'errors': errors}
        else:
            return {'success': True}

    @staticmethod
    def add_order(d, request, cart):
        user = request.user if request.user.is_authenticated else None
        if d['delivery_type'] == 'pickup':
            delivery_address = ""
        elif d['delivery_type'] == 'new_post':
            delivery_address = f'{d["delivery_settlement"]}, {d["delivery_street"]}'
        elif d['delivery_type'] in ('delivery', 'courier', 'in_time', 'avtoluks', 'ukr_post'):
            delivery_address = f'{d["delivery_obl"]} обл.,{d["delivery_settlement"]}, {d["delivery_street"]}, {d["delivery_house"]}'
        else:
            delivery_address = ""

        new_order = Order.objects.create(user=user,
                                         first_name=d['first_name'],
                                         last_name=d['last_name'],
                                         phone=d['phone'],
                                         email=d['email'],
                                         delivery_type=d['delivery_type'],
                                         payment_type=d['payment_type'],
                                         comment=d['comment'],
                                         currency_data=get_currency_data_for_order(request),
                                         delivery_address=delivery_address
                                         )

        cart.items.update(order_fk_id=new_order.id)
        new_order.total = new_order.get_total_price()
        new_order.save(add_order_status=True)
        cart.flush_items()
        cart.refresh_fields()
        # notify_admin_about_order(new_order, request)
        # notify_buyer_about_order(new_order, request)
        # TODO з лікпейом треба ше порішати
        if new_order.payment_type == 'liqpay':
            request.session['order_id'] = new_order.id
            from apps.checkout.api import send_liqpay
            s = send_liqpay(request)
            return {'success': True, 'payment': True, 'button': s}
        if not user:
            del request.session['cart_id']
        return {'success': True, 'payment': False, "order": new_order}


class CartItem(models.Model):
    qty = models.DecimalField(verbose_name=_('admin__qty'), default=1.00, max_digits=9, decimal_places=2)
    current_price = models.DecimalField(verbose_name=_('admin__total_price'), max_digits=9, decimal_places=2, default=0.00)
    stable_price = models.DecimalField(verbose_name=_('admin__total_price'), max_digits=9, decimal_places=2, default=0.00)
    product_fk = models.ForeignKey('products.Product', verbose_name=_('admin__product'), on_delete=models.SET_NULL, null=True)
    option_of_product_mtm = ChainedManyToManyField(OptionOfProduct, related_name='option_of_product_mtm', help_text='', chained_field="product_fk", chained_model_field="product_fk", blank=True)
    order_fk = models.ForeignKey(Order, verbose_name=_('admin__product'), on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _('admin__cart_item')
        verbose_name_plural = _('admin__cart_items')

    @property
    def discount(self):
        d = Discount.objects.filter(product_fk_id=self.product_fk_id).first()
        return d.get_text if d else None

    @property
    def one_item_price(self):
        return self.current_price / self.qty

    @property
    def options(self):
        options_of_product = self.option_of_product_mtm.all()
        result = []
        for option_of_product in options_of_product:
            result.append({'option_name': option_of_product.option_fk.name, 'option_value_name': option_of_product.option_value_fk.value})
        return result

    @property
    def stock_rest(self):
        qty = None
        for o_o_p in self.option_of_product_mtm.all():
            if qty is None:
                qty = 0
                qty += o_o_p.qty
            else:
                qty += o_o_p.qty
        if qty is None:
            qty = self.product_fk.qty
        return qty

    def get_calc_item_price(self, user_id, _qty=None):
        if not _qty:
            _qty = self.qty
        product_price = self.product_fk.get_price(user_id=user_id, options=self.option_of_product_mtm.all())
        print(product_price)
        return {
            'current_price': Decimal(product_price['current_price']) * int(_qty),
            'stable_price': Decimal(product_price['stable_price']) * int(_qty),
            'discount_value': product_price['discount_value']
        }

    def __str__(self):
        try:
            return self.product_fk.__str__()
        except Exception as ex:
            return str(self.id)


class OrderStatus(models.Model):
    code = models.CharField(verbose_name=_("admin__order_code"), max_length=255, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0])
    date = models.DateTimeField(verbose_name=_("admin__date"), auto_now_add=True)
    order_fk = models.ForeignKey(Order, verbose_name=_("admin_order_fk"), on_delete=models.CASCADE)
    notify_user = models.BooleanField(verbose_name=_("admin_notify_user"), default=True)

    class Meta:
        verbose_name = _("admin__order_status")
        verbose_name_plural = _("admin__orders_status")

    @property
    def name(self):
        try:
            return dict(ORDER_STATUS_CHOICES)[self.code]
        except Exception as e:
            return self.code

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(OrderStatus, self).save()
        print('qwe')
        if self.notify_user:
            try:
                o = OrderMessageTemplate.objects.get(keyword=self.code)
                o.send_message(self.order_fk)
            except Exception as e:
                print('-----------', str(e))
                pass

    def __str__(self):
        return str(self.code)


# TODO ЗЛАМАНО бо удалив функцію з ордер_інфо
class OrderMessageTemplate(models.Model):
    keyword = models.CharField(verbose_name=_("admin__status"), max_length=255, choices=ORDER_STATUS_CHOICES, unique=True)
    text = RichTextField(verbose_name=_("admin__text"), null=True, blank=True, default="")
    subject = models.CharField(verbose_name=_("admin__subject"), max_length=255, blank=False)

    class Meta:
        verbose_name = _("admin__order_message_template")
        verbose_name_plural = _("admin__orders_message_templates")

    def send_message(self, order, ):
        request = get_request()
        import time
        start_time = time.time()
        dict_order = order.__dict__
        for i in dict_order.keys():
            self.text = self.text.replace(f"\x7B%{i}%\x7D", str(dict_order[i]))
            self.subject = self.subject.replace(f'\x7B%{i}%\x7D', str(dict_order[i]))
        host_url = 'https://' + request.get_host()
        self.text = self.text.replace('{%products%}', render_to_string('checkout/emails/order_products_list.html', {'items': order.cartitem_set.all(), 'order': order, "host_url": host_url}))
        notify_buyer_thread = threading.Thread(target=send_html_mail, args=(self.subject, self.text, dict_order['email']))
        notify_buyer_thread.start()
        notify_admin_thread = threading.Thread(target=send_html_mail, args=(self.subject, self.text, Email.objects.filter(keyword='checkout').first().email))
        notify_admin_thread.start()
        # send_html_mail(self.subject, self.text, dict_order['email'])
        print("--- %s seconds ---" % (time.time() - start_time))


# @receiver([m2m_changed], sender=CartItem.option_of_product_mtm.through)
def post_m2m_changer_cart_item(sender, instance, *args, **kwargs):
    if instance.order_fk is not None:
        post_save.disconnect(post_save_cart_item, sender=CartItem)
        instance.total_price = instance.get_calc_item_price() * instance.qty
        instance.save()
        post_save.connect(post_save_cart_item, sender=CartItem)
        order = Order.objects.get(id=instance.order_fk.id)
        total_price = order.get_total_price()
        order.total = total_price
        order.save()


# TODO провірити нахуя це тут і чи работає
# @receiver([post_save, post_delete], sender=CartItem)
def post_save_cart_item(sender, instance, *args, **kwargs):
    try:
        if instance.order_fk is not None:
            m2m_changed.disconnect(post_m2m_changer_cart_item, sender=CartItem)
            order = Order.objects.get(id=instance.order_fk.id)
            cart_items = CartItem.objects.filter(order_fk_id=order.id)
            instance.total_price = instance.product_fk.get_price_by_options(instance.option_of_product_mtm.all()) * instance.qty
            post_save.disconnect(post_save_cart_item, sender=CartItem)
            instance.save()
            post_save.connect(post_save_cart_item, sender=CartItem)
            total_price = order.get_total_price()
            order.total = total_price
            order.save()
    except Exception as ex:
        print("Error post_save_cart_item()", ex)
        ValueError(ex)


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, verbose_name=_('admin__items'))
    items_count = models.IntegerField(verbose_name=_('admin__items_count'), default=0)
    total_price = models.DecimalField(verbose_name=_('admin__total_price'), max_digits=9, decimal_places=2, default=0.00)

    def flush_items(self):
        for item in self.items.all():
            self.items.remove(item)
        self.save()

    def refresh_fields(self):
        if self.items.count() > 0:
            suma = 0
            for _item in self.items.all():
                price_data = _item.get_calc_item_price(user_id=None, _qty=_item.qty)
                suma += price_data['current_price']
                _item.stable_price = price_data['stable_price']
                _item.current_price = price_data['current_price']
                _item.save()
            # response = self.items.aggregate(Sum('current_price'))
            count = self.items.aggregate(Sum('qty'))
            self.total_price = suma
            self.items_count = count['qty__sum']
        else:
            self.total_price = 0.00
            self.items_count = 0
        self.save(update_fields=['total_price', 'items_count'])

    def add_item_to_cart(self, _product_id, _user_id, _qty, _options=None, ):
        _qty = Decimal(_qty)
        product = Product.objects.get(id=_product_id)  # Товарна позиція яка приходить в фукнції
        cart_items = self.items.filter(product_fk_id=product.id)  # Всі CartItem в яких товарна позиція product
        if not _qty or _qty < product.min_unit:
            _qty = product.min_unit
        check_result = product.check_for_required_options(_options)
        if check_result is not True:
            return {'success': False, 'required': check_result}  # Повернення незаповнених опцій
        elif cart_items:
            # ------ Шукаємо в корзині хоча б один CartItem з таким Product
            for _item in cart_items:  # Цикл по CartItem
                if _item.qty + _qty > _item.stock_rest:
                    return {'success': False, 'message': _('Out_of_stock')}
                options_1 = list(_item.option_of_product_mtm.all().values_list('id', flat=True))
                options_2 = list(_options.values_list('id', flat=True))
                # ----- Якщо опції CartItem співпадають з опціями товару який прийшов в функцію
                if options_1 == options_2:
                    _item.qty += Decimal(_qty)
                    price_data = _item.get_calc_item_price(user_id=_user_id, _qty=_item.qty)
                    _item.current_price = price_data['current_price']
                    _item.stable_price = price_data['stable_price']
                    _item.save()
                    self.refresh_fields()
                    return {'success': True, 'object': _item, 'cart_items_count': self.items_count, 'cart_total_price': self.total_price}

        # ----- Опції не співпадають - тому створюємо новий CartItem
        _item = CartItem.objects.create(product_fk=product, qty=_qty)
        if _options:
            [_item.option_of_product_mtm.add(opt) for opt in _options]
        price_data = _item.get_calc_item_price(user_id=_user_id, _qty=_qty)
        _item.current_price = price_data['current_price']
        _item.stable_price = price_data['stable_price']
        _item.save()
        self.items.add(_item)
        self.refresh_fields()
        return {'success': True, 'object': _item, 'cart_items_count': self.items_count, 'cart_total_price': self.total_price}

    def remove_item_from_cart(self, cart_item_id):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            self.items.remove(cart_item)
            self.refresh_fields()
            return {'success': True, 'cart_items_count': self.items_count, 'cart_total_price': self.total_price}
        except Exception as ex:
            return {'success': False, 'message': str(ex)}

    def change_item_qty(self, _user_id, item_id, operation):
        try:
            _item = CartItem.objects.get(id=item_id, order_fk__isnull=True)
            unit = _item.product_fk.unit.min_amount
            if operation['name'] == 'plus':
                if _item.qty + unit > _item.stock_rest:
                    return {'success': False, 'message': _('Out_of_stock')}
                _item.qty += unit
            elif operation['name'] == 'minus' and _item.qty > unit:
                _item.qty -= unit
            elif operation['name'] == 'assign':
                _item.qty = operation['value']
            price_data = _item.get_calc_item_price(user_id=_user_id, _qty=_item.qty)
            _item.current_price = price_data['current_price']
            _item.stable_price = price_data['stable_price']
            _item.save()
            self.refresh_fields()
            return {'success': True, 'cart_items_count': self.items_count, 'cart_total_price': self.total_price}
        except Exception as e:
            print(str(e))
        # print('CHANGE_ITEM_QTY: ', str(e))
        # return {'success': False}

    class Meta:
        verbose_name = _('admin__cart')
        verbose_name_plural = _('admin__carts')
