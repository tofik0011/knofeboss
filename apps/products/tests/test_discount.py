import datetime
from django.test import RequestFactory, TestCase, Client
from apps.products.models import Product, Category, Discount


class TestProduct(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create()
        self.product = Product.objects.create(category_fk_id=self.category.id, price=1000.00)

    def test_discount(self):
        now = datetime.datetime.now()
        d = Discount.objects.create(percentage=50,
                                    product_fk_id=product.id,
                                    start_date=now - datetime.timedelta(days=1),
                                    end_date=now + datetime.timedelta(days=1)
                                    )
        print('sss', self.product.calc_price)
        self.assertEqual(product.calc_price, 500.00)
