from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ContactsConfig(AppConfig):
    name = 'apps.contacts'
    verbose_name = _('admin__contacts')
