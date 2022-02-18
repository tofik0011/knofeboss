from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.products.models import Product, AttributeOfProduct


class Comparison(models.Model):
    products = models.ManyToManyField(Product, verbose_name=_('admin__products'), blank=True)

    def get_attributes_ids(self):
        return list(AttributeOfProduct.objects.filter(product_fk_id__in=self.get_products_ids()).values_list('attribute_fk_id', flat=True).distinct())

    def get_products_ids(self):
        return list(self.products.all().values_list('id', flat=True))

    def add_product(self, product_id):
        if int(product_id) in self.get_products_ids():
            return {'success': False, 'error': 'already_in_comparison'}
        self.products.add(Product.objects.get(id=product_id))
        return {'success': True}

    def has_product(self, product_id):
        products = self.get_products_ids()
        if product_id in products:
            return True
        else:
            return False

    def del_product(self, product_id):
        try:
            product = Product.objects.get(id=product_id)
            self.products.remove(product)
            return {'success': True}
        except Exception as e:
            return {'success': False}
