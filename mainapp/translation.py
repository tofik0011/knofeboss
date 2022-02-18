from modeltranslation.translator import register, translator, TranslationOptions

from unine_engine.settings import LANGUAGES
from .models import TextContent, SeoData, Settings, GoogleMap


@register(TextContent)
class TextContentTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)
    required_languages = [lang[0] for lang in LANGUAGES]


@register(SeoData)
class SeoDataTranslationOptions(TranslationOptions):
    fields = ('seo_title', 'seo_description',)
    required_languages = [lang[0] for lang in LANGUAGES]

@register(Settings)
class SettingsTranslationOptions(TranslationOptions):
    fields = ('formula_for_seo_generation_title', 'formula_for_seo_generation_description',)
    # required_languages = [lang[0] for lang in LANGUAGES]
