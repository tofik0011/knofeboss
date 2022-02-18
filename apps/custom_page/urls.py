from django.urls import re_path
from .views import view__custom_page

urlpatterns = [
    re_path(r'(?P<slug>[\w\d\W]+)/$', view__custom_page, name='view__custom_page'),
]
