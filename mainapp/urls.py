from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page

from .views import *
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap, index as sitemap_index
from .sitemaps import ArticleSitemap, StaticSitemap, ArticleCategorySitemap, CustomPageSitemap, ProductSitemap, ProductCategorySitemap

sitemaps = {
    'static': StaticSitemap,  # add StaticSitemap to the dictionary
    'ArticleCategorySitemap': ArticleCategorySitemap,
    'ArticleSitemap': ArticleSitemap,
    'CustomPageSitemap': CustomPageSitemap,
    'ProductSitemap': ProductSitemap,
    'ProductCategorySitemap': ProductCategorySitemap,
}

urlpatterns = [
    path('', get_index_page, name="index"),
    path('robots.txt', get_robots_txt, name="robots_file"),
    path('contacts/', get_contacts_page, name="view__contacts"),
    path('production/', view__production, name="view__production"),
    path('api_google_map/', api_google_map, name="api_google_map"),
    path('home/', igreen, name="igreen"),
    path('home_b/', igreen_b, name="igreen_b"),
    path('sitemap1.xml', cache_page(86400)(sitemap_index), {'sitemaps': sitemaps, 'template_name': 'sitemap_index_custom.xml'}),
    path('sitemap1-<section>.xml', cache_page(86400)(sitemap), {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # re_path(r'^sitemap1-(?P<section>.+).xml$', {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]
