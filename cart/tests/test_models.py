from django.test import TestCase
from ..factory import (
    UserFactory,
    CategoryFactory,
    ProductFactory,
    CartFactory,
    CartItemFactory,
)
from ..models import Cart, CartItem
from decimal import Decimal


class CartModelTest(TestCase):
    def setUp(self):
        self.cart = CartFactory()
        self.product1 = ProductFactory(price=Decimal("19.99"))
        self.product2 = ProductFactory(price=Decimal("4.78"))
        self.cartitem1 = CartItemFactory(
            cart=self.cart, product=self.product1, quantity=1
        )
        self.cartitem2 = CartItemFactory(
            cart=self.cart, product=self.product2, quantity=2
        )

    def test_cart_total_price_calculation(self):
        self.assertEqual(self.cart.total_price, Decimal("29.55"))

        cart = CartFactory()
        self.assertEqual(cart.total_price, 0)

    def test_cart_total_quantity_calculation(self):
        self.assertEqual(self.cart.total_quantity, 3)

        cart = CartFactory()
        self.assertEqual(cart.total_quantity, 0)

    def test_cart_item_total_price_calculation(self):
        self.assertEqual(
            self.cartitem2.item_total_price,
            self.product2.price * self.cartitem2.quantity,
        )

    def test_cart_str_with_user(self):
        user = UserFactory()
        self.cart.user = user
        self.assertEqual(str(self.cart), "Cart user_0")

    def test_cart_str_with_session(self):
        self.cart.session_key = "e12ewk1"
        self.assertEqual(str(self.cart), "Cart e12ewk1")

    def test_cart_total_price_after_quantity_change(self):
        self.cartitem1.quantity = 10
        self.cartitem1.save()

        self.cart.refresh_from_db()

        self.assertEqual(
            self.cart.total_price,
            sum(
                [self.product1.price * self.cartitem1.quantity,
                self.product2.price * self.cartitem2.quantity]
            ),
        )
