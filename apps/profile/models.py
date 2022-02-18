from django.contrib.auth import authenticate, update_session_auth_hash
from django.core.paginator import Paginator
from django.db import models
from filebrowser.fields import FileBrowseField
from apps.checkout.models import Cart, Order
from django.contrib.auth.models import User, AbstractUser, Group
from apps.logger.app import add_log
from apps.products.get_data import get_products_field
from apps.products.models import Product
from mainapp.helper import validate_email, validate_phone
from unine_engine.globals import USER_TYPES
from django.utils.translation import ugettext_lazy as _


class GroupProxy(Group):
    class Meta:
        proxy = True
        auto_created = True
        verbose_name = _('group_proxy')
        verbose_name_plural = _("groups_proxy")


class TypeProfile(models.Model):
    type = models.CharField(verbose_name=_("admin_profile_type"), max_length=255)
    percent_discount = models.IntegerField(verbose_name=_('admin__percent_discount'), default=0, blank=True, null=True)
    min_price = models.DecimalField(verbose_name=_('admin__min_price'), max_digits=9, decimal_places=2, default=0, blank=True, null=True)
    default = models.BooleanField(verbose_name=_('admin__default'), default=False)
    keyword = models.CharField(verbose_name=_("admin_type_keyword"), max_length=255)

    class Meta:
        verbose_name = _('admin_type_profile')
        verbose_name_plural = _('admin_type_profiles')

    def __str__(self):
        return self.type

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.default is True:
            TypeProfile.objects.all().update(default=False)
        super(TypeProfile, self).save()


class Profile(AbstractUser):
    type_profile_fk = models.ForeignKey(TypeProfile, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(verbose_name=_("admin_phone"), max_length=255, default="", blank=True)
    wishlist = models.ManyToManyField(Product, verbose_name=_("admin_wishlist"), blank=True)
    picture = FileBrowseField(verbose_name=_('admin__image'), max_length=255, directory="profile/", extensions=[".jpg", ".png"], blank=True)
    cart = models.OneToOneField(Cart, verbose_name=_('admin__cart'), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        try:
            return f'{self.first_name} {self.last_name}'
        except Exception:
            return str(self.id)

    class Meta:
        verbose_name = _('admin_profile')
        verbose_name_plural = _('admin_profiles')

    def has_in_wishlist(self, product_id):
        """Есть ли товар у пользователя в списке желаний"""
        ids = self.wishlist.all().values_list('id', flat=True)
        return True if product_id in ids else False

    def del_product_from_wishlist(self, product_id):
        """Удаление товара из списка желаний"""
        try:
            self.wishlist.remove(Product.objects.get(id=product_id))
            self.save()
            return True
        except Exception as e:
            add_log(str(e), self.del_product_from_wishlist.__name__)
            return False

    def add_product_to_wishlist(self, product_id):
        """Добавление товара в списка желаний"""
        try:
            self.wishlist.add(Product.objects.get(id=product_id))
            self.save()
            return True
        except Exception as e:
            add_log(str(e), self.add_product_to_wishlist.__name__)
            return False

    def get_wishlist(self, page=1, limit=6):
        """Получение товаров из списка желаний"""
        ids = self.wishlist.all().values_list('id', flat=True)
        data, paginator = get_products_field(products_ids=ids, page=page, limit=limit)
        return data, paginator.has_next()

    def get_orders_list(self, page=1, limit=1):
        """Получение списка заказов пользователя"""
        orders_list = Order.objects.filter(user_id=self.id).order_by('-date')
        pagination_data = Paginator(orders_list, limit).page(page)
        return pagination_data

    def edit_profile_data(self, data, request):
        errors = []
        # email = data.get('email', None)
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        phone = data.get('phone', None)
        account_type = data.get('account_type', None)
        current_password = data.get('current_password', None)
        new_password = data.get('new_password', None)
        re_password = data.get('re_password', None)

        if not first_name:
            errors.append({'#first_name': _('error__required_field')})

        if not last_name:
            errors.append({'#last_name': _('error__required_field')})

        if not phone:
            errors.append({'#phone': _('error__required_field')})
        elif not validate_phone(phone):
            errors.append({'#phone': _('error__invalid_phone')})

        if not account_type:
            errors.append({'#account_type': _('error__required_field')})

        if not current_password:
            errors.append({'#current_password': _('error__required_field')})
        elif not self.check_password(current_password):
            errors.append({'#current_password': _('error__invalid_credentials')})

        if new_password or re_password:
            if len(new_password) < 6:
                errors.append({'#new_password': _('error__min_length').format(6)})
            if new_password != re_password:
                errors.append({'#re_password': _('error__passwords_are_not_equal')})

        if len(errors) > 0:
            return {'success': False, 'errors': errors}
        else:
            print(account_type)
            self.phone = phone
            self.type_profile_fk = TypeProfile.objects.filter(keyword=account_type).first()
            self.first_name = first_name
            self.last_name = last_name
            if new_password:
                self.set_password(new_password)
                update_session_auth_hash(request, self)
            self.save()
            return {'success': True}

    @staticmethod
    def authentication_form_validate(data, request):
        errors = []
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username.lower(), password=password)
        if not user or not user.check_password(password):
            errors.append({'#password': _('error__invalid_credentials')})
        if len(errors) > 0:
            return {'success': False, 'errors': errors}
        else:
            return {'success': True, 'user': user}

    @staticmethod
    def registration_form_validate(data, request):
        errors = []

        email = data.get('email', None)
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        phone = data.get('phone', None)
        account_type = data.get('account_type', None)
        password = data.get('password', None)
        re_password = data.get('re_password', None)

        if not email:
            errors.append({'#email': _('error__required_field')})
        elif not validate_email(email):
            errors.append({'#email': _('error__invalid_email')})
        elif Profile.objects.filter(username__iexact=email.lower()).exists():
            errors.append({'#email': _('error__email_is_already_in_use')})

        if not first_name:
            errors.append({'#first_name': _('error__required_field')})
        if not last_name:
            errors.append({'#last_name': _('error__required_field')})

        if not phone:
            errors.append({'#phone': _('error__required_field')})
        elif not validate_phone(phone):
            errors.append({'#phone': _('error__invalid_phone')})

        if not account_type:
            errors.append({'#account_type': _('error__required_field')})

        if not password:
            errors.append({'#password': _('error__required_field')})
        elif len(password) < 6:
            errors.append({'#password': _('error__min_length').format(6)})
        if not re_password:
            errors.append({'#re_password': _('error__required_field')})
        elif password != re_password:
            errors.append({'#re_password': _('error__passwords_are_not_equal')})
        return errors

    @staticmethod
    def create_user(d):
        print(d)
        profile = Profile(username=d['email'].lower(),
                          first_name=d['first_name'],
                          last_name=d['last_name'],
                          email=d['email'].lower(),
                          phone=d['phone'],
                          type_profile_fk=TypeProfile.objects.filter(keyword=d['account_type']).first(),)


        profile.set_password(d['password'])
        profile.save()
        return profile
