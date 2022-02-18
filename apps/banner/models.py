from django.db import models
from django.utils.translation import ugettext_lazy as _
from filebrowser.fields import FileBrowseField
from unine_engine import settings

CONTENT_POSITIONS = (
    ('left', u'left'),
    ('center', u'center'),
    ('right', u'right'),
)
BANNERS_KEYWORD = (
    ('mainpage', _('admin__mainpage')),
    ('mainpage_second', _('admin__mainpage_second')),
    ('mainpage_third', _('admin__mainpage_third')),
)


class Banner(models.Model):
    keyword = models.CharField(verbose_name=_("admin__keyword"), choices=BANNERS_KEYWORD, max_length=255, unique=True)

    active = models.BooleanField(verbose_name=_("admin__active"), default=True)
    image = FileBrowseField(verbose_name=_('admin__image'), max_length=255, directory="banners/", extensions=[".jpg", ".png"], blank=True)
    content_text = models.CharField(verbose_name=_("admin__content_text"), max_length=255, blank=True)
    button_link = models.CharField(verbose_name=_("admin__button_link"), max_length=255, blank=True)

    class Meta:
        verbose_name=_("admin__banner_model")
        verbose_name_plural=_("admin__banners_model")