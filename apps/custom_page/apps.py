from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomPageConfig(AppConfig):
    name = 'apps.custom_page'
    verbose_name = _('admin__custom_pages')
