from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import Article, Category as ArticleCategory
from apps.products.models import Product, Category as ProductCategory
from apps.custom_page.models import CustomPage

PROTOCOL = 'http'


class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1
    protocol = PROTOCOL

    def items(self):
        return [
            'index',
            'blog',
            'view__contacts',
            'view__production',
            'catalog',
            'specials',
            'view__search',
            'view__testimonials',
        ]

    def location(self, item):
        return reverse(item)


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = PROTOCOL
    limit = 1000

    def items(self):
        return Article.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return obj.get_absolute_url()


class ArticleCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = PROTOCOL

    def items(self):
        return ArticleCategory.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return obj.get_absolute_url()


class CustomPageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1
    protocol = PROTOCOL

    def items(self):
        return CustomPage.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return obj.get_absolute_url()


class ProductCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 1
    protocol = PROTOCOL

    def items(self):
        return ProductCategory.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return obj.get_absolute_url()


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    protocol = PROTOCOL
    limit = 1000

    def items(self):
        return Product.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return obj.get_absolute_url()
