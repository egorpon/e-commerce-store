from django.test import TestCase, RequestFactory
from ..factory import (
    UserFactory,
    CategoryFactory,
    ProductFactory,
    CartFactory,
    CartItemFactory,
)
from ..models import Cart, CartItem
from ..cart import CartService
from decimal import Decimal

# Create your tests here.


class CartServiceTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory(name="shoes", slug="shoes")
        self.product = ProductFactory()

        factory = RequestFactory()

        request = factory.get("/")
        request.user = self.user
        request.session = self.client.session

        self.service = CartService(request)

    def test_add_product_to_cart(self):
        self.service.add(self.product, 2)
        cart = Cart.objects.filter(user=self.user).first()
        item = CartItem.objects.filter(cart=cart, product=self.product).first()

        self.assertIsNotNone(item)
        self.assertEqual(item.quantity, 2)

    def test_add_existing_product_updates_quantity(self):
        self.service.add(self.product, 2)
        self.service.add(self.product, 5)

        cart = Cart.objects.filter(user=self.user).first()
        item = CartItem.objects.filter(cart=cart, product=self.product).first()

        self.assertEqual(item.quantity, 5)

    def test_delete_product(self):
        self.service.add(self.product, 2)

        self.service.delete(self.product.id)

        cart = Cart.objects.filter(user=self.user).first()
        item = CartItem.objects.filter(cart=cart, product=self.product).first()

        self.assertIsNone(item)

    def test_update_changes_product_quantity(self):
        self.service.add(self.product, 1)

        self.service.update(self.product.id, 5)

        cart = Cart.objects.filter(user=self.user).first()
        item = CartItem.objects.filter(cart=cart, product=self.product).first()

        self.assertEqual(item.quantity, 5)

    def test_len_returns_count_of_products(self):
        product_1 = ProductFactory(title="Nike")

        self.service.add(self.product, 1)
        self.service.add(product_1, 5)

        self.assertEqual(len(self.service), 6)

    def test_cart_iter_yield_correct_data(self):
        self.service.add(self.product, 2)
        
        for item in self.service:
            self.assertEqual(item["product"], self.product)
            self.assertEqual(item['quantity'], 2)
            self.assertEqual(item['total'], round(Decimal(self.product.price * 2),2))


    def test_get_total_calculates_amount(self):
        self.service.add(self.product, 2)
        
        self.assertEqual(self.service.get_total(), round(Decimal(self.product.price * 2),2))

    def test_get_item_total_calculates_item_amount(self):
        product_1 = ProductFactory(title="Nike")

        self.service.add(self.product, 1)
        self.service.add(product_1, 5)

        self.assertEqual(self.service.get_item_total(product_1.id), round(Decimal(product_1.price * 5),2))