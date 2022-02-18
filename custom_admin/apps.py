from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class MainappConfig(AppConfig):
    name = 'custom_admin'
    verbose_name = _('admin__custom_admin')
