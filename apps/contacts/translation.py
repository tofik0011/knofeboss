from modeltranslation.translator import register, translator, TranslationOptions

from unine_engine.settings import LANGUAGES
from .models import Address


@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ('address',)
    required_languages = [lang[0] for lang in LANGUAGES]