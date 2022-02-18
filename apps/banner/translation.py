from modeltranslation.translator import register, translator, TranslationOptions

from unine_engine.settings import LANGUAGES
from .models import Banner


@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ('image', 'content_text',  'button_link',)
    required_languages = [lang[0] for lang in LANGUAGES]

