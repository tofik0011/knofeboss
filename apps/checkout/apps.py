from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CheckoutConfig(AppConfig):
    name = 'apps.checkout'
    verbose_name = _('admin__checkout')
