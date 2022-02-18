from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FeedbackFormConfig(AppConfig):
    name = 'apps.feedback_form'
    verbose_name = _('feedback_form')
