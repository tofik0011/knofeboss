from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NewsletterConfig(AppConfig):
    name = 'apps.newsletter'
    verbose_name = _('admin__news_letter')
