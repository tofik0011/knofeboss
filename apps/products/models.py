import json
import operator
from functools import reduce

import numpy
import os
from datetime import datetime, timedelta
from operator import concat
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from slugify import slugify
from smart_selects.db_fields import ChainedManyToManyField, ChainedForeignKey

from django_currentuser.middleware import get_current_user
from unine_engine import globals
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Min, Avg, Count, Q
from django.db.models.signals import post_save, post_delete, post_init, pre_save
from django.dispatch import receiver, Signal
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from filebrowser.fields import FileBrowseField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from decimal import Decimal
from unine_engine.globals import LANGUAGES, OPTION_OPERATION, PRODUCTS_PER_PAGE, PRODUCTS_SORTING, DISCOUNT_CHOICES
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

# Create your models here.
from django.urls import reverse

# from django.db.models import
## агрегатные функции ##
# from django.db.models.aggregates import Aggregate # определение
# from django.db.models.sql import constants.Aggregate# import Aggregate as SQLAggregate # реализация

from django.db.models import Aggregate


class Concat(Aggregate):
    function = 'GROUP_CONCAT'
    # template = '%(function)s(%(distinct)s%(expressions)s)'
    allow_distinct = True

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=models.CharField(),
            **extra
        )


class Category(MPTTModel):
    image = FileBrowseField(verbose_name=_('admin__image'), max_length=255, directory="category/", extensions=[".jpg", ".png", ".webp"], default="default/no_image.jpg", blank=True)
    active_in_mainpage = models.BooleanField(verbose_name=_('Відображення на головній '), default=False, null=False)
    image_banner = FileBrowseField(verbose_name=_('image_banner'), max_length=255, directory="category/", extensions=[".jpg", ".png", ".webp"], default="", blank=True)
    order = models.IntegerField(verbose_name=_('admin__order'), default=0)
    h1 = models.CharField(verbose_name=_("admin__h1"), max_length=255, null=True, blank=True, default="")
    id_1c = models.CharField(verbose_name=_('admin__id_1c'), blank=True, null=True, max_length=255, default="")
    link = models.CharField("URL", null=False, max_length=255)
    name = models.CharField(verbose_name=_('admin__name'), null=False, max_length=255)
    seo_title = models.CharField(verbose_name=_('admin__seo_title'), null=True, blank=True, max_length=255, default='')
    seo_description = models.TextField(verbose_name=_('admin__seo_description'), null=True, blank=True, default='')
    description = RichTextField(verbose_name=_('admin__description'), null=True, blank=True, default='')
    active = models.BooleanField(verbose_name=_('admin__active'), default=True, null=False)
    parent = TreeForeignKey('self', verbose_name=_('admin__parent'), null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    added_date = models.DateTimeField(verbose_name=_('admin__added_date'), auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(verbose_name=_('admin__update_date'), auto_now_add=False, auto_now=True)


    class MPTTMeta:
        level_attr = 'level'
        order_insertion_by = ['order']

    class Meta:
        verbose_name = _('admin__category')
        verbose_name_plural = _('admin__categories')

    def save(self, *args, **kwargs):
        for lang in LANGUAGES:
            self.__setattr__(f'link_{lang[0]}', slugify(self.__getattribute__(f'link_{lang[0]}'), to_lower=True))
        super(Category, self).save(*args, **kwargs)

    #
    # def save(self, *args, **kwargs):
    #     super(Category, self).save(*args, **kwargs)
    #     # Category.objects.rebuild()
    #
    # def delete(self, *args, **kwargs):
    #     super(Category, self).delete(*categorylanguageargs, **kwargs)
    #     # Category.objects.rebuild()

    def __str__(self):
        try:
            return self.name
        except Exception as ex:
            return str(self.id)

    def get_all_children_and_your_father(self):
        children = [self]
        try:
            child_list = self.children.all()
        except AttributeError:
            return children
        for child in child_list:
            children.extend(child.get_all_children_and_your_father())
        return children

    def get_all_children(self):
        all_children = self.get_all_children_and_your_father()
        all_children.remove(all_children[0])
        return all_children

    def get_all_parents(self):
        parents = [self]
        if self.parent is not None:
            parent = self.parent
            parents.extend(parent.get_all_parents())
        return parents

    def get_absolute_url(self):
        link = ""
        for parent in reversed(self.get_all_parents()):
            link += parent.link + "/"
        link = link[:-1]
        return reverse('product_or_category', args=[str(link)])

    def clean(self):
        if self.parent in self.get_all_children():
            raise ValidationError("Error Category")

    @staticmethod
    def get_category_by_link(link):
        try:
            category = Category.objects.get(active=True, link=link)
            category.redirect = False
        except Exception as ex:
            q_list = [Q(**{f"link_{lang[0]}": link}) for lang in LANGUAGES]
            category = Category.objects.filter(reduce(operator.or_, q_list)).first()
            category.redirect = True
        return category

    @staticmethod
    def get_all_categories(is_parents=True):
        """ Віддає всі включенні категорії (is_parents=True Тільки батьків) """
        if is_parents:
            categories = Category.objects.filter(active=True, parent=None)
        else:
            categories = Category.objects.filter(active=True)
        for category in categories:
            category.count_products = Product.objects.filter(category_fk_id=category.id, active=True).count()
        return categories


class Unit(models.Model):
    min_amount = models.DecimalField(verbose_name=_('admin__min_amount'), max_digits=9, decimal_places=2)
    symbol = models.CharField(verbose_name=_('admin__symbol_unit'), max_length=255, blank=True, null=True)
    name = models.CharField(verbose_name=_('admin__name_unit'), max_length=255, blank=True, null=True)

    def __str__(self):
        try:
            return str(self.name)
        except Exception as e:
            return str(self.id)

    class Meta:
        verbose_name = _('admin__unit')
        verbose_name_plural = _('admin__unit')


class Product(models.Model):
    id_import = models.CharField(verbose_name=_('admin__id_import'), null=True, max_length=40, blank=True)
    article = models.CharField(verbose_name=_('admin__article_p'), null=True, max_length=255, blank=True)
    unit = models.ForeignKey(Unit, verbose_name=_('admin__unit'), on_delete=models.CASCADE, null=True)
    image = FileBrowseField(verbose_name=_('admin__image'), max_length=255, directory="products/", extensions=[".jpg", ".png", ".webp"], default="default/no_image.jpg", blank=True)
    active = models.BooleanField(verbose_name=_('admin__active'), default=True)
    price = models.DecimalField(verbose_name=_('admin__price'), null=True, blank=True, decimal_places=2, max_digits=9, default=0.00)
    calc_price = models.DecimalField(verbose_name=_('admin__calc_price'), null=True, blank=True, decimal_places=2, max_digits=9, default=None)
    lowest_option_price = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=9, default=None)
    show_in_categories = models.ManyToManyField(Category, verbose_name=_('admin__show_in_categories'), blank=True)
    similar = models.ManyToManyField('self', verbose_name=_('admin__similar'), blank=True)
    qty = models.IntegerField(verbose_name=_('admin__qty'), blank=True, null=True, default=1)
    is_bestseller = models.BooleanField(verbose_name=_('admin__is_bestseller'), default=False)
    is_special = models.BooleanField(verbose_name=_('admin__is_special'), default=False)
    rating = models.IntegerField(verbose_name=_('admin__rating'), null=True, blank=True, default=0)
    link = models.CharField(verbose_name=_('admin__link'), null=False, max_length=255)
    name = models.CharField(verbose_name=_('admin__name'), null=False, max_length=255)
    description = RichTextField(verbose_name=_('admin__description'), null=True, blank=True, default="")
    seo_title = models.CharField(verbose_name=_('admin__seo_title'), null=True, blank=True, max_length=255)
    seo_description = models.CharField(verbose_name=_('admin__seo_description'), null=True, blank=True, max_length=400)
    category_fk = models.ForeignKey(Category, verbose_name=_('admin__category'), on_delete=models.CASCADE, related_name='category_fk')
    added_date = models.DateTimeField(verbose_name=_('admin__added_date'), auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(verbose_name=_('admin__update_date'), auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _('admin__product')
        verbose_name_plural = _('admin__products')

    def __str__(self):
        try:
            return self.name
        except Exception as ex:
            return str(self.id)

    @property
    def color(self):
        try:
            return self.attributeofproduct_set.get(attribute_fk__keyword='color').attribute_value_fk.get_name()
        except Exception as e:
            return None

    @property
    def similar_products(self):
        return self.similar.all()

    @property
    def min_unit(self):
        return self.unit.min_amount

    @property
    def images(self):
        return self.productimage_set.values('image')

    @property
    def attributes(self):
        result = []
        attrs_of_prod = AttributeOfProduct.objects.filter(product_fk_id=self.id).order_by('attribute_fk_id')

        for attr_of_prod in attrs_of_prod:
            try:
                attr = attr_of_prod.attribute_fk
                attr_val = attr_of_prod.attribute_value_fk

                result.append({
                    'attr_pk': attr.id,
                    'product_pk': attr_of_prod.product_fk.id,
                    'attr_value_pk': attr_val.id,
                    'name': attr.name,
                    'value': attr_val.value,
                })
            except Exception as ex:
                print(ex)
        return result

    @staticmethod
    def get_product_by_link(link):
        try:
            product = Product.objects.get(active=True, link=link)
            product.redirect = False
        except Exception as ex:
            q_list = [Q(**{f"link_{lang[0]}": link}) for lang in LANGUAGES]
            product = Product.objects.filter(reduce(operator.or_, q_list)).first()
            product.redirect = True
        return product

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        d = Discount.objects.filter(product_fk_id=self.id).first()
        _lowest_option_price = self.get_lowest_option_price()
        if d:
            if d.type == 'percentage':
                self.calc_price = _lowest_option_price - (_lowest_option_price * d.value / 100)
            elif d.type == 'sum':
                self.calc_price = _lowest_option_price - d.value
        else:
            self.calc_price = _lowest_option_price
        self.lowest_option_price = _lowest_option_price
        super(Product, self).save()

    def get_reviews(self, page=1):
        """ Повертає масив затверджених відгуків """
        reviews = Review.objects.filter(product_fk_id=self.id, is_approved=True).values('name', 'text', 'rating', 'added_date').order_by('-added_date')
        paginator = Paginator(reviews, globals.REVIEWS_PER_PAGE)
        result = paginator.get_page(page)
        return result

    def refresh_rating(self):
        """ Оновлення рейтингу товару. Викликається сигналом після збереження відгуку """
        reviews = Review.objects.filter(is_approved=True).aggregate(avg=Avg('rating'), count=Count('id'))
        self.rating = reviews['avg']
        super(Product, self).save()

    def get_lowest_option_price(self):
        option_price = self.price
        options_of_product = OptionOfProduct.objects.filter(product_fk_id=self.id, option_fk__required=True, price__isnull=False)
        if options_of_product:
            temp = options_of_product.values_list('option_fk__id', 'option_fk__operation', named=True, flat=False).order_by('-option_fk__operation').distinct()
            for opt in temp:
                cheapest_equal_price = options_of_product.filter(product_fk_id=self.id, option_fk_id=opt.option_fk__id, option_fk__required=True).aggregate(min_price=Min('price'))
                if opt.option_fk__operation == 'equal':
                    option_price = cheapest_equal_price['min_price']
                elif opt.option_fk__operation == 'add':
                    option_price = option_price + cheapest_equal_price['min_price']

            return option_price
        else:
            return self.price

    def options(self, options_of_product=None):
        try:
            if options_of_product is None:
                options_of_product = OptionOfProduct.objects.filter(product_fk_id=self.id)
                if not options_of_product:
                    return None
            _temp = []
            result = []
            for option_of_product in options_of_product:
                option = option_of_product.option_fk
                option_val = option_of_product.option_value_fk
                _temp.append({  # OptionOfProduct
                    'option_pk': option.pk,
                    'option_name': option.name,
                    'option_keyword': option.keyword,
                    'is_required': option.required,
                    'option_value_name': option_val.value,
                    'option_value_pk': option_of_product.option_value_fk.pk,
                    'option_of_product_pk': option_of_product.pk,
                    'product_pk': self.pk,
                    'option_price': option_of_product.price,
                    'operation': option_of_product.option_fk.operation,
                    # 'option_price_calculated': option_of_product.product_fk.get_discount_price(option_of_product.product_fk.price + option_of_product.price),
                    'option_qty': option_of_product.qty,
                })

            options_temp = []

            for option_of_product in _temp:
                if not any(d['option_pk'] == option_of_product['option_pk'] for d in options_temp):
                    options_temp.append({
                        'option_pk': option_of_product['option_pk'],
                        'option_name': option_of_product['option_name'],
                        'option_keyword': option_of_product['option_keyword'],
                        'option_price': option_of_product['option_price'],
                        'operation': option_of_product['operation'],
                        'is_required': option_of_product['is_required'],
                    })

            for option in options_temp:
                values = [oop for oop in _temp if oop['option_pk'] == option['option_pk']]
                _values = sorted(values, key=lambda d: 0.00 if not d['option_price'] else d['option_price'])
                result.append({
                    'option_pk': option['option_pk'],
                    'option_name': option['option_name'],
                    'option_keyword': option['option_keyword'],
                    'is_required': option['is_required'],
                    'values': _values
                })

            return result
        except Exception as e:
            print(f'{e}, ----- {__name__}')
        return None

    def check_for_required_options(self, options_objects):
        required_options_ids = OptionOfProduct.objects.filter(option_fk__required=True, product_fk_id=self.id).values_list('option_fk_id', flat=True)
        if required_options_ids:
            if options_objects:
                received_options_ids = set(options_objects.values_list('option_fk_id', flat=True).order_by('option_fk_id'))
                result = set(required_options_ids) - received_options_ids
                return result if result else True
            else:
                return required_options_ids
        else:
            return True

    def get_absolute_url(self):
        return str(self.category_fk.get_absolute_url() + str(self.link) + "/")

    def get_product_discount(self):
        return Discount.objects.filter(product_fk_id=self.id, end_date__gt=now()).last()

    def get_price(self, user_id=None, options=None):
        # from apps.profile.models import Profile
        user = get_current_user()
        result = {}
        try:
            product_discount = self.get_product_discount()
            if not options or options is None:
                stable_price = self.get_lowest_option_price()
            else:
                stable_price = self.get_price_by_options(options)

            if user.is_authenticated:
                if user.type_profile_fk:
                    if user.type_profile_fk.default is True:
                        result.update({
                            'current_price': round(stable_price if not product_discount else product_discount.get_discounted_price(stable_price), 2),
                        })
                        result.update({'discount_value': None if not product_discount else product_discount.get_text, })
                    else:
                        result.update({'current_price': round(stable_price - stable_price * Decimal((user.type_profile_fk.percent_discount / 100)), 2)})
                        result.update({'discount_value': f"{user.type_profile_fk.percent_discount}%"})
                else:
                    result.update({'current_price': round(stable_price if not product_discount else product_discount.get_discounted_price(stable_price), 2), })
                    result.update({'discount_value': None if not product_discount else product_discount.get_text, })
            else:
                result.update({'current_price': round(stable_price if not product_discount else product_discount.get_discounted_price(stable_price), 2), })
                result.update({'discount_value': None if not product_discount else product_discount.get_text, })
            result.update({'stable_price': round(stable_price, 2)})

            return result

        except Exception as e:
            print('GET_PRICE: ', str(e))
            return {}

    def get_price_by_options(self, options=None):
        price = self.price
        # if not options or options is None:
        #     options = self.optionofproduct_set.all()

        if options and options is not None:
            equal_option = options.values_list('price', named=True).filter(option_fk__operation='equal').first()
            add_options = options.values_list('option_fk__operation', 'price', named=True).filter(option_fk__operation='add')
            if equal_option and equal_option.price is not None: price = equal_option.price
            for option in add_options:
                if option.price is not None:
                    price += option.price
            return price
        else:
            return price


class ProductImage(models.Model):
    image = FileBrowseField(verbose_name=_('admin__image'), max_length=200, directory="products/", extensions=[".jpg", ".webp", ".png"], blank=True)
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('admin__product_image')
        verbose_name_plural = _('admin__product_images')

    def __str__(self):
        return str(self.image)


class Discount(models.Model):
    product_fk = models.OneToOneField(Product, verbose_name=_('admin__product'), on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name=_('admin__start_date'), default=datetime.now, auto_now_add=False, auto_now=False)
    end_date = models.DateTimeField(verbose_name=_('admin__end_date'), auto_now_add=False, auto_now=False, default=datetime.now() + timedelta(days=1))
    type = models.CharField(verbose_name=_('admin__type'), max_length=255, choices=DISCOUNT_CHOICES)
    value = models.DecimalField(verbose_name=_('admin__value'), max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = _('admin__discount')
        verbose_name_plural = _('admin__discounts')

    @property
    def get_text(self):
        if self.type == 'percentage':
            return f'-{self.value}%'
        elif self.type == 'sum':
            return self.value

    def get_discounted_price(self, stable_price=None):
        if not stable_price:
            stable_price = self.product_fk.price
        if self.type == 'percentage':
            return round(stable_price - (stable_price * self.value / 100), 2)
        elif self.type == 'sum':
            return round(stable_price - self.value, 2)

    def clean(self):
        _lowest_option_price = self.product_fk.get_lowest_option_price()
        calc_price = 0.00
        if self.type == 'percentage':
            calc_price = _lowest_option_price - (_lowest_option_price * self.value / 100)
        elif self.type == 'sum':
            calc_price = _lowest_option_price - self.value
        if calc_price <= 0.00:
            print(calc_price)
            raise ValidationError({'value': "Цена < 0.00"})
        if self.start_date >= self.end_date:
            raise ValidationError({'end_date': "Некорректная дата"})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.end_date > timezone.now():
            self.product_fk.is_special = True
        else:
            self.product_fk.is_special = False
        self.product_fk.save()
        super(Discount, self).save()


class Option(models.Model):  # КОЛІР, ВАГА, ШИРИНА
    keyword = models.CharField(verbose_name=_('admin__keyword'), null=False, max_length=255)
    operation = models.CharField(verbose_name=_('admin__operation'), max_length=20, choices=OPTION_OPERATION)
    required = models.BooleanField(verbose_name=_('admin__required'), default=False)
    show_in_filters = models.BooleanField(verbose_name=_('admin__show_in_filters'), default=True)
    name = models.CharField(verbose_name=_('admin__name'), null=False, max_length=255)

    class Meta:
        verbose_name = _('admin__option')
        verbose_name_plural = _('admin__options')

    def __str__(self):
        try:
            if self.operation == 'add':
                index = ' (+)'
            elif self.operation == 'equal':
                index = ' (=)'
            else:
                index = ''
            return str(self.keyword + index + "*") if self.required else str(self.keyword + index)
        except Exception as ex:
            return str(self.id)


class OptionValue(models.Model):
    id_1c = models.CharField(verbose_name=_('admin__id_1c'), null=True, max_length=255, blank=True)
    option_fk = models.ForeignKey(Option, verbose_name=_('admin__option'), on_delete=models.CASCADE)
    value = models.CharField(verbose_name=_('admin__value'), null=False, max_length=255)  # RED, BLACK, GREEN

    class Meta:
        verbose_name = _('admin__option_value')
        verbose_name_plural = _('admin__option_values')

    def __str__(self):
        name = self.id
        try:
            name = self.value
        except Exception as ex:
            ValueError(ex)
        return str(name)


# TODO кількість тоже треба рахувати в юнітах
class OptionOfProduct(models.Model):
    option_fk = models.ForeignKey(Option, verbose_name=_('admin__option'), on_delete=models.CASCADE)
    product_fk = models.ForeignKey(Product, verbose_name=_('admin__product'), on_delete=models.CASCADE)
    option_value_fk = ChainedForeignKey(OptionValue, verbose_name=_('admin__option_value'), chained_field="option_fk", chained_model_field="option_fk", show_all=False, auto_choose=True,
                                        sort=True, blank=True)
    qty = models.IntegerField(verbose_name=_('admin__qty'), default=1)
    price = models.DecimalField(verbose_name=_('admin__price'), null=True, blank=True, decimal_places=2, max_digits=9, default=None)

    def __str__(self):
        return str(self.option_fk.__str__())

    class Meta:
        verbose_name = _('admin__option_of_product')
        verbose_name_plural = _('admin__options_of_products')
        unique_together = ['option_fk', 'product_fk', 'option_value_fk']


@receiver([post_save, post_delete], sender=Product)
def post_edit_product(sender, instance, *args, **kwargs):
    pass
    # print('PRODUCT')


@receiver([post_save, post_delete], sender=Discount)
def post_edit_discount(sender, instance, *args, **kwargs):
    print('DISCOUNT')
    instance.product_fk.save()
    print('END_SAVE2', instance.product_fk.calc_price)


@receiver([pre_save, post_delete], sender=OptionOfProduct)
def post_edit_option_of_product(sender, instance, *args, **kwargs):
    print('OPTION OF PRODUCT')
    post_save.disconnect(receiver=post_edit_option_of_product, sender=OptionOfProduct, dispatch_uid=None)
    instance.product_fk.save()
    post_save.connect(receiver=post_edit_option_of_product, sender=OptionOfProduct, dispatch_uid=None)


class Attribute(models.Model):
    id_1c = models.CharField(verbose_name=_('admin__id_1c'), null=True, max_length=100, blank=True)
    keyword = models.CharField(verbose_name=_('admin__keyword'), null=False, max_length=100)
    show_in_filters = models.BooleanField(verbose_name=_('admin__show_in_filters'), default=True)
    name = models.CharField(verbose_name=_('admin__name'), null=False, max_length=100)

    def __str__(self):
        name = self.id
        try:
            name = self.name
        except Exception as ex:
            ValueError(ex)
        return str(name)

    class Meta:
        verbose_name = _('admin__attribute')
        verbose_name_plural = _('admin__attributes')


class AttributeValue(models.Model):
    id_1c = models.CharField(verbose_name=_('admin__id_1c'), null=True, max_length=100, blank=True)
    attribute_fk = models.ForeignKey(Attribute, verbose_name=_('admin__attribute'), on_delete=models.CASCADE)
    value = models.CharField(verbose_name=_('admin__value'), null=False, max_length=100)

    class Meta:
        verbose_name = _('admin__attribute_value')
        verbose_name_plural = _('admin__attributes_values')

    def __str__(self):
        name = self.id
        try:
            name = self.value
        except Exception as ex:
            ValueError(ex)
        return str(name)


class AttributeOfProduct(models.Model):
    attribute_fk = models.ForeignKey(Attribute, verbose_name=_('admin__attribute'), on_delete=models.CASCADE)
    product_fk = models.ForeignKey(Product, verbose_name=_('admin__product'), on_delete=models.CASCADE)
    attribute_value_fk = ChainedForeignKey(AttributeValue, verbose_name=_('admin__attribute_value'), chained_field="attribute_fk", chained_model_field="attribute_fk", show_all=False, auto_choose=True,
                                           sort=True, blank=True)

    def __str__(self):
        return str(self.attribute_fk.__str__())

    class Meta:
        verbose_name = _('admin__attribute_of_product')
        verbose_name_plural = _('admin__attributes_of_products')
        unique_together = ['attribute_fk', 'product_fk']


class Filter(models.Model):
    name = models.CharField(verbose_name=_('admin__name'), null=False, max_length=100)

    def __str__(self):
        name = self.id
        try:
            name = self.name
        except Exception as ex:
            ValueError(ex)
        return str(name)

    class Meta:
        verbose_name = _('admin__filter')
        verbose_name_plural = _('admin__filters')


class FilterValue(models.Model):
    filter_fk = models.ForeignKey(Filter, verbose_name=_('admin__filter'), on_delete=models.CASCADE)
    value = models.CharField(verbose_name=_('admin__value'), null=False, max_length=255)

    class Meta:
        verbose_name = _('admin__filter_value')
        verbose_name_plural = _('admin__filters_values')

    def __str__(self):
        value = self.id
        try:
            value = self.value
        except Exception as ex:
            ValueError(ex)
        return str(value)


class FilterOfProduct(models.Model):
    filter_fk = models.ForeignKey(Filter, verbose_name=_('admin__filter'), on_delete=models.CASCADE)
    product_fk = models.ForeignKey(Product, verbose_name=_('admin__product'), on_delete=models.CASCADE)
    filter_value_fk = ChainedForeignKey(FilterValue, verbose_name=_('admin__filter_value'), chained_field="filter_fk", chained_model_field="filter_fk", show_all=False, auto_choose=True,
                                        sort=True, blank=True)

    def __str__(self):
        return str(self.filter_fk.__str__())

    class Meta:
        verbose_name = _('admin__filter_of_product')
        verbose_name_plural = _('admin__filters_of_products')


class Review(models.Model):
    name = models.CharField(verbose_name=_('admin__name'), null=False, max_length=100)
    text = models.TextField(verbose_name=_('admin__review'), null=False)
    rating = models.IntegerField(verbose_name=_('admin__rating'), default=5, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    product_fk = models.ForeignKey(Product, verbose_name=_('admin__product'), on_delete=models.CASCADE)
    is_approved = models.BooleanField(verbose_name=_('admin__is_approved'), default=False)
    added_date = models.DateTimeField(verbose_name=_('admin__added_date'), auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = _('admin__review')
        verbose_name_plural = _('admin__reviews')


@receiver([post_save, post_delete], sender=Review)
def post_edit_review(sender, instance, *args, **kwargs):
    product = instance.product_fk
    product.refresh_rating()
