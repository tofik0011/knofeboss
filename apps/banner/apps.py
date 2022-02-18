from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class BannerConfig(AppConfig):
    name = 'apps.banner'
    verbose_name=_('admin__banner')
