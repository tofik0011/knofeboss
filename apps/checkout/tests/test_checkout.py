import json
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse, resolve
from apps.profile.models import Profile
from apps.checkout.api import add_to_cart, remove_from_cart
from apps.checkout.get_data import get_cart
from apps.checkout.models import Cart, CartItem
from apps.checkout.views import Checkout
import pytest
from mixer.backend.django import mixer
from apps.products.models import Product, Category


class TestAPI(TestCase):

    def setUp(self):
        self.client_logged = Client()
        self.client_anon = Client()
        self.user = User.objects.create_user(username='javed', email='javed@javed.com', password='my_secret')
        self.account = Profile.objects.create(user_fk_id=self.user.id)
        self.category = Category.objects.create()
        self.product = Product.objects.create(category_fk_id=self.category.id)
        self.cart_item = CartItem.objects.create(product_fk_id=self.product.id)
        self.client_logged.user = self.user
        self.client_logged.get(reverse('index'))
        self.client_anon.user = AnonymousUser()
        self.client_anon.get(reverse('index'))
        self.cart_anonymous = Cart.objects.create()

    def test_add_to_cart(self):
        res = self.client_logged.post(reverse('add_to_cart'), data={'product_id': 1})
        data = json.loads(res.content)
        self.assertEqual(True, data['success'])
        self.assertEqual(1, data['cart_items_count'])

    def test_remove_from_cart_logged(self):
        self.client_logged.user.account.cart = Cart.objects.create()
        self.client_logged.user.account.cart.items.add(self.cart_item)
        res = self.client_logged.post(reverse('remove_from_cart'), data={'cart_item_id': 1})
        data = json.loads(res.content)
        self.assertEqual(True, data['success'])
        self.assertEqual(0, data['cart_items_count'])
        self.assertEqual('0.00', data['cart_total_price'])

    def test_remove_from_cart_anonymous(self):
        cart = get_cart(self.client_anon)
        cart.items.add(self.cart_item)
        res = self.client_anon.post(reverse('remove_from_cart'), data={'cart_item_id': 1})
        data = json.loads(res.content)
        self.assertEqual(True, data['success'])
        self.assertEqual(0, data['cart_items_count'])
        self.assertEqual('0.00', data['cart_total_price'])


