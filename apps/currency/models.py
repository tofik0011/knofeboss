from django.db import models
from mainapp.models import Settings
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    name = models.CharField(verbose_name=_("admin__name_currency"), max_length=20, default="")
    code = models.CharField(verbose_name=_("admin__code"), max_length=20, default="")
    symbol_left = models.CharField(verbose_name=_("admin__symbol_left"), max_length=6, blank=True, default='')
    symbol_right = models.CharField(verbose_name=_("admin__symbol_right"), max_length=6, blank=True, default='')
    value = models.DecimalField(verbose_name=_("admin__value"), max_digits=10, decimal_places=4, default=0.0000)
    status = models.BooleanField(verbose_name=_("admin__status"), max_length=20, default=True)
    is_default = models.BooleanField(verbose_name=_("admin__is_default"), blank=True, default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_default is True:
            Currency.objects.exclude(id=self.id).update(is_default=False)
        elif self.is_default is False:
            if len(Currency.objects.filter(is_default=True)) == 0:
                self.is_default = True
        super(Currency, self).save()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _("admin__currency")
        verbose_name_plural = _("admin__currencies")
