from __future__ import unicode_literals
from django import template
from apps.profile.models import Profile

register = template.Library()


# @register.simple_tag
# def tag_get_user_data(request):
#     account = Account.objects.get(user_fk_id=request.user.id)
#     return account


@register.simple_tag
def tag_get_user_wishlist(request):
    wishlist, has_next_page = request.user.get_wishlist()
    return {'wishlist': wishlist, 'has_next_page': has_next_page}


@register.simple_tag
def tag_get_orders_list(request):
    return request.user.get_orders_list()
