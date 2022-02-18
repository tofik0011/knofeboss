from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CurrencyConfig(AppConfig):
    name = 'apps.currency'
    verbose_name = _('admin__currency')
