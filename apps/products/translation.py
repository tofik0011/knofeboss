from modeltranslation.translator import register, translator, TranslationOptions

from unine_engine.settings import LANGUAGES
from .models import Category, Product, Filter, FilterValue, Attribute, AttributeValue, OptionValue, Option, Unit


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('link', 'name', 'seo_title', 'seo_description', 'description', 'image_banner', 'h1')
    required_languages = {'default':('link', 'name',)}


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('link', 'name', 'seo_title', 'seo_description', 'description')
    required_languages = [lang[0] for lang in LANGUAGES]


@register(Filter)
class FilterTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = [lang[0] for lang in LANGUAGES]


@register(FilterValue)
class FilterValueTranslationOptions(TranslationOptions):
    fields = ('value',)
    required_languages = [lang[0] for lang in LANGUAGES]


@register(Attribute)
class AttributeTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = [lang[0] for lang in LANGUAGES]


@register(AttributeValue)
class AttributeValueTranslationOptions(TranslationOptions):
    fields = ('value',)
    required_languages = [lang[0] for lang in LANGUAGES]


@register(Option)
class OptionTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = [lang[0] for lang in LANGUAGES]


@register(OptionValue)
class OptionValueTranslationOptions(TranslationOptions):
    fields = ('value',)
    required_languages = [lang[0] for lang in LANGUAGES]


@register(Unit)
class UnitTranslationOptions(TranslationOptions):
    fields = ('symbol', 'name')
    required_languages = [lang[0] for lang in LANGUAGES]