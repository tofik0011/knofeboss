import operator
from functools import reduce

from django.db.models import Q
from slugify import slugify

from unine_engine.globals import LANGUAGES
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import get_language
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from ckeditor_uploader.fields import RichTextUploadingField


class CustomPage(MPTTModel):
    order = models.PositiveIntegerField(verbose_name=_('admin__order'), default=0)
    active = models.BooleanField(verbose_name=_('admin__active'), default=True)
    parent = TreeForeignKey('self', verbose_name=_('admin__parent'), null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    link = models.CharField(verbose_name=_('admin__link'), null=False, max_length=255)
    name = models.CharField(verbose_name=_('admin__name'), null=False, max_length=255)
    description = RichTextUploadingField(verbose_name=_('admin__description'), null=True, blank=True, default="")
    seo_title = models.CharField(verbose_name=_('meta_title'), null=True, blank=True, default="", max_length=255)
    seo_description = models.TextField(verbose_name=_('meta_description'), null=True, blank=True, default="")
    added_date = models.DateTimeField(verbose_name=_('admin__added_date'), auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(verbose_name=_('admin__update_date'), auto_now_add=False, auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        verbose_name = _('admin__custom_page')
        verbose_name_plural = _('admin__custom_pages')

    def save(self, *args, **kwargs):
        for lang in LANGUAGES:
            self.__setattr__(f'link_{lang[0]}', slugify(self.__getattribute__(f'link_{lang[0]}'), to_lower=True))
        super(CustomPage, self).save(*args, **kwargs)
        CustomPage.objects.rebuild()

    def delete(self, *args, **kwargs):
        super(CustomPage, self).delete(*args, **kwargs)
        CustomPage.objects.rebuild()

    def __str__(self):
        try:
            return str(self.name)
        except Exception as ex:
            return str(self.id)

    def get_all_children_and_your_father(self):
        children = [self]
        try:
            child_list = self.children.all()
        except AttributeError:
            return children
        for child in child_list:
            children.extend(child.get_all_children_and_your_father())
        return children

    def get_all_children(self):
        all_children = self.get_all_children_and_your_father()
        all_children.remove(all_children[0])
        return all_children

    def get_absolute_url(self):
        link = ""
        data = list(self.get_ancestors(include_self=True))
        for parent in data:
            link += parent.link + "/"
        link = link[:-1]
        return reverse('view__custom_page', args=[str(link)])

    @staticmethod
    def get_custompage_by_url(link):
        """ Віддає дані статті по ссилці"""
        try:
            c_page = CustomPage.objects.get(active=True, link=link)
            c_page.redirect = False
        except Exception as ex:
            q_list = [Q(**{f"link_{lang[0]}": link}) for lang in LANGUAGES]
            c_page = CustomPage.objects.filter(reduce(operator.or_, q_list)).first()
            c_page.redirect = True
        return c_page

    def clean(self):
        if self.parent in self.get_all_children():
            raise ValidationError("Error CustomPage")
