from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from unine_engine.globals import MENU_CHOICES


class MenuItem(MPTTModel):
    order = models.PositiveIntegerField(verbose_name=_("admin__order"), default=0, null=False)
    active = models.BooleanField(verbose_name=_("admin__active"), default=True)
    parent = TreeForeignKey('self', verbose_name=_("admin__parent_menu"), null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    link = models.CharField(verbose_name=_('admin__link'), max_length=255, default="", blank=True,
                            help_text=_("Пример: '/ru/catalog/'. Указывать со / вначале и в конце. Код языка также указывается (кроме ссылок на основном языке сайта)."))
    title = models.CharField(verbose_name=_('admin__title'), max_length=255, default="", blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(MenuItem, self).save(*args, **kwargs)
        MenuItem.objects.rebuild()

    def delete(self, *args, **kwargs):
        super(MenuItem, self).delete(*args, **kwargs)
        MenuItem.objects.rebuild()

    def clean(self):
        order = MenuItem.objects.filter(order=self.order, level=self.level).exclude(id=self.id).exists()
        if order:
            raise ValidationError({'order': _(f"Номер пункта меню уже используется")})

    class MPTTMeta:
        # left_attr = 'rght'
        # right_attr = 'lft'
        level_attr = 'level'
        # order_insertion_by = ['order', 'menu_keyword']

    class Meta:
        verbose_name = _("admin__menu_item")
        verbose_name_plural = _("admin__menu_items")
        # ordering = ['menu_keyword', 'order']


class MenuItemTOP(MPTTModel):
    order = models.PositiveIntegerField(verbose_name=_("admin__order"), default=0, null=False)
    active = models.BooleanField(verbose_name=_("admin__active"), default=True)
    parent = TreeForeignKey('self', verbose_name=_("admin__parent_menu"), null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    link = models.CharField(verbose_name=_('admin__link'), max_length=255, default="", blank=True,
                            help_text=_("Пример: '/ru/catalog/'. Указывать со / вначале и в конце. Код языка также указывается (кроме ссылок на основном языке сайта)."))
    title = models.CharField(verbose_name=_('admin__title'), max_length=255, default="", blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(MenuItemTOP, self).save(*args, **kwargs)
        MenuItemTOP.objects.rebuild()

    def delete(self, *args, **kwargs):
        super(MenuItemTOP, self).delete(*args, **kwargs)
        MenuItemTOP.objects.rebuild()

    def clean(self):
        order = MenuItemTOP.objects.filter(order=self.order, level=self.level).exclude(id=self.id).exists()
        if order:
            raise ValidationError({'order': _(f"Номер пункта меню уже используется")})

    class MPTTMeta:
        # left_attr = 'rght'
        # right_attr = 'lft'
        level_attr = 'level'
        # order_insertion_by = ['order', 'menu_keyword']

    class Meta:
        verbose_name = _("admin__menu_item_top")
        verbose_name_plural = _("admin__menu_items_top")
        # ordering = ['menu_keyword', 'order']

