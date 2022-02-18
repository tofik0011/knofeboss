from modeltranslation.translator import register, translator, TranslationOptions

from unine_engine.settings import LANGUAGES
from .models import Article, Category


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('link', 'name', 'seo_title', 'seo_description', 'short_description', 'description', 'image')
    required_languages = {'default': ('link', 'name',)}
    # required_languages = [lang[0] for lang in LANGUAGES]



@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('link', 'name', 'seo_title', 'seo_description', 'description')
    required_languages = {'default': ('link', 'name',)}

