from django.test import TestCase
from .factory import (
    UserFactory,
    CategoryFactory,
    ProductFactory,
    CartFactory,
    CartItemFactory,
)
from .models import Cart, CartItem
from django.urls import reverse

# Create your tests here.


class CartViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory(name="shoes", slug="shoes")
        self.product = ProductFactory()

    def test_cart_add_with_authorized_user(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("cart_add"),
            {"product_id": self.product.id, "product_quantity": 1, "action": "post"},
        )
        response = self.client.post(
            reverse("cart_add"),
            {"product_id": self.product.id, "product_quantity": 2, "action": "post"},
        )

        self.assertEqual(response.status_code, 200)

        user_cart = Cart.objects.filter(user=self.user).first()
        self.assertIn(
            self.product.id, user_cart.items.values_list("product", flat=True)
        )

        self.assertEqual(user_cart.items.count(), 1)

        cart_item = CartItem.objects.filter(
            cart=user_cart, product=self.product
        ).first()
        self.assertEqual(cart_item.quantity, 2)

    def test_cart_add_with_unauthorized_user(self):
        self.client.post(
            reverse("cart_add"),
            {"product_id": self.product.id, "product_quantity": 1, "action": "post"},
        )
        response = self.client.post(
            reverse("cart_add"),
            {"product_id": self.product.id, "product_quantity": 2, "action": "post"},
        )

        self.assertEqual(response.status_code, 200)

        session_key = self.client.session.session_key
        user_cart = Cart.objects.filter(session_key=session_key).first()
        self.assertIn(
            self.product.id, user_cart.items.values_list("product", flat=True)
        )

        self.assertEqual(user_cart.items.count(), 1)

        cart_item = CartItem.objects.filter(
            cart=user_cart, product=self.product
        ).first()
        self.assertEqual(cart_item.quantity, 2)

    def test_cart_update_with_authorized_user(self):
        self.client.force_login(self.user)
        cart = CartFactory(user=self.user)
        cart_item = CartItemFactory(cart=cart, product=self.product, quantity=1)

        response = self.client.post(
            reverse("cart_update"),
            {"product_id": self.product.id, "product_quantity": 5, "action": "post"},
        )

        self.assertEqual(response.status_code, 200)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)

    def test_cart_update_with_unauthorized_user(self):
        session_key = self.client.session.session_key
        cart = CartFactory(session_key=session_key)
        cart_item = CartItemFactory(cart=cart, product=self.product, quantity=1)

        response = self.client.post(
            reverse("cart_update"),
            {"product_id": self.product.id, "product_quantity": 5, "action": "post"},
        )

        self.assertEqual(response.status_code, 200)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)

    def test_cart_delete_with_authorized_user(self):
        self.client.force_login(self.user)

        product2 = ProductFactory(title="Nike Air Force")

        cart = CartFactory(user=self.user)

        CartItemFactory(cart=cart, product=self.product, quantity=2)
        CartItemFactory(cart=cart, product=product2, quantity=5)

        response = self.client.post(
            reverse("cart_delete"), {"action": "post", "product_id": self.product.id}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.items.count(), 1)
        self.assertNotIn(self.product.id, cart.items.all().values_list('product', flat=True))
        self.assertTrue(cart.items.filter(product=product2).exists())
