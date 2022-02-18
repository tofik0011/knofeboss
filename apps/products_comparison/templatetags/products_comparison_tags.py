from django import template
from django.utils.translation import get_language
from apps.products_comparison.views import get_comparison
from apps.products.models import Product, AttributeOfProduct, Attribute, AttributeValue

register = template.Library()


def get_attr_val_by_attr_id(product_id, attribute_id):
    attr_val = AttributeOfProduct.objects.filter(product_fk_id=product_id, attribute_fk_id=attribute_id)
    return attr_val if attr_val else '-'


@register.simple_tag
def tag_get_comparison_products(request):
    comparison = get_comparison(request)
    products = Product.objects.filter(id__in=comparison.get_products_ids())
    attr_ids = comparison.get_attributes_ids()
    products_data = []
    for pr in products:
        attr_of_product = []
        for attr_id in attr_ids:
            attr_of_product.append(get_attr_val_by_attr_id(pr.id, attr_id))
        products_data.append({
            'fields': pr.__dict__,
            'attrs': attr_of_product,
            'attributes': pr.attributes,
        })
    attributes = Attribute.objects.filter(id__in=attr_ids,)
    data = {
        'attributes': attributes,
        'products': products_data,
    }
    return data
