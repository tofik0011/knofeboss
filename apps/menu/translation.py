from modeltranslation.translator import register, translator, TranslationOptions

from unine_engine.settings import LANGUAGES
from .models import MenuItem, MenuItemTOP


@register(MenuItem)
class MenuItemTranslationOptions(TranslationOptions):
    fields = ('link', 'title',)
    required_languages = [lang[0] for lang in LANGUAGES]\

@register(MenuItemTOP)
class MenuItemTOPTranslationOptions(TranslationOptions):
    fields = ('link', 'title',)
    required_languages = [lang[0] for lang in LANGUAGES]
