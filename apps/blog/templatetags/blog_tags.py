from django import template
from ..models import Category, Article

register = template.Library()


@register.simple_tag
def tag_last_articles(limit=100):
    """Тег для получення останіх стетей блогу"""
    return Article.get_last_articles(limit=limit)


@register.simple_tag
def tag_categories():
    """Тег для получення всіх батьківських категорій"""
    return Category.get_all_categories()
