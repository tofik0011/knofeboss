from slugify import slugify
from unine_engine.settings import LANGUAGES
from .models import Article


def action_copy_article(modeladmin, request, queryset):
    for article in queryset:
        _temp_article = article
        _temp_article.pk = None
        _temp_article.active = False
        _temp_article.save()
        for lang in LANGUAGES:
            _temp_article.__setattr__(f'link_{lang[0]}', f"{slugify(_temp_article.__getattribute__(f'link_{lang[0]}'), to_lower=True)}_new_{_temp_article.id}")
        _temp_article.save()
