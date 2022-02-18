from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DeliveryConfig(AppConfig):
    name = 'apps.nova_poshta'
    verbose_name = _('admin__delivery')
