from django.core.exceptions import ValidationError
from django.db import models
from filebrowser.fields import FileBrowseField, FileBrowseUploadField
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from unine_engine.globals import LANGUAGES, TEXT_CONTENT_KEYWORDS, MENU_CHOICES, SEO_DATA_KEYWORDS
from django.utils.translation import ugettext_lazy as _, get_language


class Settings(models.Model):
    name = models.CharField(verbose_name=_('admin__name'), max_length=20, blank=True, default='Another Shop')
    logo = FileBrowseField(verbose_name=_('admin__logo'), max_length=200, directory="logo/", extensions=[".jpg", ".png", ".webp"], blank=True)
    favicon = FileBrowseField(verbose_name=_('fav_icon'), max_length=200, directory="/", extensions=[".png", ".ico"], blank=True)
    robots_txt = models.TextField('Robots.txt', null=True, blank=True, default="")
    sitemap = FileBrowseField('Sitemap', null=True, blank=True, default="", max_length=255, directory="sitemaps/", extensions=['.xml'])
    google_analytics_code = models.TextField(verbose_name=_('admin__google_analytics'), null=True, blank=True, default="")
    formula_for_seo_generation_title = models.TextField(verbose_name=_('formula_for_seo_generation_title'), null=True, blank=True, default="")
    formula_for_seo_generation_description = models.TextField(verbose_name=_('formula_for_seo_generation_description'), null=True, blank=True, default="")


    class Meta:
        verbose_name = _("admin__settings")
        verbose_name_plural = _("admin__settings")


class TextContent(models.Model):
    keyword = models.CharField(verbose_name=_("admin__keyword"), choices=TEXT_CONTENT_KEYWORDS, max_length=255, blank=True, default=None, unique=True)
    title = models.CharField(verbose_name=_("admin__title"), max_length=255, blank=True, default="")
    description = RichTextUploadingField(verbose_name=_("admin__description"), null=True, blank=True, default="")

    class Meta:
        verbose_name = _("admin__text_content")
        verbose_name_plural = _("admin__text_contents")


class SeoData(models.Model):
    keyword = models.CharField(verbose_name=_("admin__keyword"), choices=SEO_DATA_KEYWORDS, max_length=255, blank=True, default=None, unique=True)
    seo_title = models.CharField(verbose_name=_('admin__title'), null=False, max_length=255)
    seo_description = models.TextField(verbose_name=_('admin__description'), null=True, blank=True, default="")

    class Meta:
        verbose_name = _("admin__seo_data")
        verbose_name_plural = _("admin__seo_data")


class GoogleMap(models.Model):
    name_marker = models.CharField(verbose_name=_("admin__name_marker"), max_length=255, blank=True, default=None,)
    lat = models.FloatField(verbose_name=_("admin__lng"), null=False, max_length=20)
    longitude = models.FloatField(verbose_name=_("admin__longitude"), null=False, max_length=20)

    class Meta:
        verbose_name = _("admin__google_map")
        verbose_name_plural = _("admin__google_map")