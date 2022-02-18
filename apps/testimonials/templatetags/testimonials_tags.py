from django import template
from django.utils.translation import get_language

from apps.testimonials.models import Testimonial

register = template.Library()


@register.simple_tag
def tag_get_testimonials(qty=None):
    testimonials = Testimonial.objects.filter(active=True).all()
    if qty:
        testimonials = testimonials[:qty]
    return testimonials
