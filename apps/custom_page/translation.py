from modeltranslation.translator import register, translator, TranslationOptions

from unine_engine.settings import LANGUAGES
from .models import CustomPage


@register(CustomPage)
class CustomPageTranslationOptions(TranslationOptions):
    fields = ('link', 'name', 'description', 'seo_title', 'seo_description')
    required_languages = [lang[0] for lang in LANGUAGES]

