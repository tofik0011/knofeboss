import operator
from functools import reduce
from django.db.models import Q
from slugify import slugify
from django.utils.translation import get_language
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from filebrowser.fields import FileBrowseField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.conf import settings
from unine_engine.settings import LANGUAGES


class Category(MPTTModel):
    image = FileBrowseField(verbose_name=_('admin__image'), max_length=200, directory="blog/", extensions=[".jpg", ".webp", ".png", ".jpeg"], blank=True)
    order = models.PositiveIntegerField(verbose_name=_('admin__order'), default=0)
    active = models.BooleanField(verbose_name=_('admin__active'), default=True)
    link = models.CharField(verbose_name=_('admin__link'), null=False, max_length=255)
    name = models.CharField(verbose_name=_('admin__name'), null=False, max_length=255)
    seo_title = models.CharField(verbose_name=_('admin__title'), null=True, blank=True, default="", max_length=255)
    seo_description = models.TextField(verbose_name=_('admin__seo_description'),  null=True, blank=True, default="",)
    description = RichTextUploadingField(verbose_name=_('admin__description'), null=True, blank=True, default="")
    parent = TreeForeignKey('self', verbose_name=_('admin__parent'), null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    added_date = models.DateTimeField(verbose_name=_('admin__added_date'), auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(verbose_name=_('admin__update_date'), auto_now_add=False, auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        verbose_name = _('admin__category')
        verbose_name_plural = _('admin__categories')

    def save(self, *args, **kwargs):
        for lang in LANGUAGES:
            self.__setattr__(f'link_{lang[0]}', slugify(self.__getattribute__(f'link_{lang[0]}'), to_lower=True))
        super(Category, self).save(*args, **kwargs)
        Category.objects.rebuild()

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
        """ Віддає всіх дітей категорії """
        all_children = self.get_all_children_and_your_father()
        all_children.remove(all_children[0])
        return all_children

    def get_all_parents(self):
        """ Віддає всіх батьків категорії """
        parents = [self]
        if self.parent is not None:
            parent = self.parent
            parents.extend(parent.get_all_parents())
        return parents

    def get_absolute_url(self):
        link = ""
        for parent in reversed(self.get_all_parents()):
            link += parent.link + "/"
        link = link[:-1]
        return reverse('article', args=[str(link)])

    def clean(self):
        if self.parent in self.get_all_children():
            raise ValidationError("Error Category")

    @staticmethod
    def get_all_categories(is_parents=True):
        """ Віддає всі включенні категорії (is_parents=True Тільки батьків) """
        if is_parents:
            categories = Category.objects.filter(active=True, parent=None)
        else:
            categories = Category.objects.filter(active=True)
        return categories

    @staticmethod
    def get_category_by_url(link):
        try:
            category = Category.objects.get(active=True, link=link)
            category.redirect = False
        except Exception as ex:
            q_list = [Q(**{f"link_{lang[0]}": link}) for lang in LANGUAGES]
            category = Category.objects.filter(reduce(operator.or_, q_list)).first()
            category.redirect = True
        return category

    @staticmethod
    def get_all_articles_in_category(category):
        """ Віддає всі статті в категорії """
        articles = Article.objects.filter(active=True, show_in_categories=category).order_by('-id')
        return articles


class Article(models.Model):
    image = FileBrowseField(verbose_name=_('admin__article_image'), max_length=255, directory="blog/", extensions=[".jpg", ".webp", ".png", ".jpeg"], blank=True, null=True)
    category_fk = models.ForeignKey(Category, verbose_name=_('admin__article_category'), on_delete=models.CASCADE, related_name='main_category', blank=True, null=True)
    show_in_categories = models.ManyToManyField(Category, verbose_name=_('admin__article_show_in_categories'), related_name='show_in_categories', blank=True)
    active = models.BooleanField(verbose_name=_('admin__article_active'), default=True)
    link = models.CharField(verbose_name=_('admin__link'), null=False, max_length=255)
    name = models.CharField(verbose_name=_('admin__name'), null=False, max_length=255)
    seo_title = models.CharField(verbose_name=_('admin__seo_title'), null=True, blank=True, default="", max_length=255)
    seo_description = models.TextField(verbose_name=_('admin__seo_description'), null=True, blank=True, default="")
    short_description = models.TextField(verbose_name=_('admin__short_content'), null=True, blank=True, default="")
    description = RichTextUploadingField(verbose_name=_('admin__content'), null=True, blank=True, default="")
    added_date = models.DateTimeField(verbose_name=_('admin__article_added_date'), auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(verbose_name=_('admin__article_update_date'), auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _('admin__article')
        verbose_name_plural = _('admin__articles')

    def __str__(self):
        try:
            return str(self.name)
        except Exception as ex:
            return str(self.id)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        for lang in LANGUAGES:
            self.__setattr__(f'link_{lang[0]}', slugify(self.__getattribute__(f'link_{lang[0]}'), to_lower=True))
        super(Article, self).save()
        try:
            if not self.show_in_categories.filter(id=self.category_fk.id).exists():
                self.show_in_categories.add(self.category_fk)
        except Exception as ex:
            print(ex)
        super(Article, self).save()

    def get_absolute_url(self):
        if self.category_fk:
            return str(self.category_fk.get_absolute_url() + str(self.link) + "/")
        else:
            return str(reverse('article', args=[str(self.link)]))

    @staticmethod
    def get_last_articles(limit=100, current_article_id=None):
        """ Віддає всі включенні останні статті """
        if current_article_id:
            articles = Article.objects.filter(active=True).exclude(id=current_article_id).order_by('-added_date')[:limit]
        else:
            articles = Article.objects.filter(active=True).order_by('-added_date')[:limit]
        return articles

    @staticmethod
    def get_article_by_url(link):
        """ Віддає дані статті по ссилці"""
        try:
            article = Article.objects.get(active=True, link=link)
            article.redirect = False
        except Exception as ex:
            q_list = [Q(**{f"link_{lang[0]}": link}) for lang in LANGUAGES]
            article = Article.objects.filter(reduce(operator.or_, q_list)).first()
            article.redirect = True
        return article
