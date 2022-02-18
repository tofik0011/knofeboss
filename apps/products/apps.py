from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductsConfig(AppConfig):
    name = 'apps.products'
    verbose_name = _('admin__products')
