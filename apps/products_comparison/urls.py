from django.urls import re_path

from apps.products_comparison.views import view__products_comparison, add_to_comparison, del_from_comparison

urlpatterns = [
    re_path(r'^comparison/$', view__products_comparison, name="view__products_comparison"),
    re_path(r'^api/add_to_comparison/$', add_to_comparison, name="add_to_comparison"),
    re_path(r'^api/del_from_comparison/$', del_from_comparison, name="del_from_comparison"),
]
