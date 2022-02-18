import re
from django.db import models
from unine_engine.globals import PHONE_KEYWORDS, ADDRESS_KEYWORDS, EMAIL_KEYWORDS
from django.utils.translation import ugettext_lazy as _


class Email(models.Model):
    keyword = models.CharField(verbose_name=_('admin__keyword_contacts'), choices=EMAIL_KEYWORDS, max_length=64, blank=True, default=None)
    email = models.CharField(verbose_name=_('admin__email'), max_length=100, blank=True, default=None)

    class Meta:
        verbose_name = _('admin__email')
        verbose_name_plural = _('admin__emails')


class Address(models.Model):
    order = models.PositiveIntegerField(verbose_name=_('admin__order'), default=0)
    keyword = models.CharField(verbose_name=_('admin__keyword_contacts'), choices=ADDRESS_KEYWORDS, max_length=255, blank=True, default=None)
    address = models.CharField(verbose_name=_('admin__address'), max_length=150, blank=True, default=None)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = _('admin__address')
        verbose_name_plural = _('admin__addresses')

class Phone(models.Model):
    phone = models.CharField(verbose_name=_('admin__phone'), max_length=100, blank=True, default=None)
    order = models.PositiveIntegerField(verbose_name=_('admin__order'), default=0)
    keyword = models.CharField(verbose_name =_('admin__keyword_contacts'), choices=PHONE_KEYWORDS, max_length=40, blank=True, null=True)

    def __str__(self):
        return self.phone

    def get_tel_href(self):
        return re.sub(r"[() -]", "", self.phone)

    class Meta:
        verbose_name = _('admin__phone')
        verbose_name_plural = _('admin__phones')

class SocialNetwork(models.Model):
    keyword = models.CharField(verbose_name=_('admin__keyword_contacts'), max_length=100, blank=True, default=None)
    link = models.CharField(verbose_name=_('admin__link_social_network'), max_length=100, blank=True, default=None)

    def __str__(self):
        return self.keyword

    class Meta:
        verbose_name = _('admin__social_network')
        verbose_name_plural = _('admin__social_networks')
