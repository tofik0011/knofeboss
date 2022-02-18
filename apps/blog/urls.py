from django.urls import path, re_path
from .views import view__article_or_category, view__blog


urlpatterns = [
    path('blog/', view__blog, name="blog"),
    re_path(r'^blog/(?P<category_link>.+)/$', view__article_or_category, name='article'),
]
