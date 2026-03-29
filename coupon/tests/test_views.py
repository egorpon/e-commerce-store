from django.test import TestCase
from ..factory import CouponFactory
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse

from cart.factory import CartFactory, CartItemFactory, ProductFactory, CategoryFactory

from decimal import Decimal


# Create your tests here.
class CouponViewTest(TestCase):
    def setUp(self):
        self.coupon = CouponFactory(title="SAVE12")

        self.category = CategoryFactory()
        self.product = ProductFactory(category=self.category)

        self.cart = CartFactory(session_key=self.client.session.session_key)
        self.cart_item = CartItemFactory(
            cart=self.cart, product=self.product, quantity=1
        )

    def test_apply_empty_promo_code_returns_error(self):
        response = self.client.post(
            reverse("apply_coupon"), {"code": " ", "action": "post"}
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["message"], "Please enter a correct promo code")
        self.assertEqual(data["status"], "danger")

    def test_apply_non_existing_promo_code_returns_error(self):
        response = self.client.post(
            reverse("apply_coupon"), {"code": "WWWWW", "action": "post"}
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["message"], "Promo code not found")
        self.assertEqual(data["status"], "danger")

    def test_apply_expired_promo_code_returns_error(self):
        CouponFactory(
            title="OLD12",
            valid_from=timezone.now() - timedelta(days=5),
            valid_to=timezone.now() - timedelta(days=1),
        )
        response = self.client.post(
            reverse("apply_coupon"), {"code": "OLD12", "action": "post"}
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["message"], "This promo code has expired")
        self.assertEqual(data["status"], "danger")

    def test_apply_already_applied_promo_code_returns_error(self):
        self.client.post(
            reverse("apply_coupon"), {"code": "SAVE12", "action": "post"}
        )
        response = self.client.post(
            reverse("apply_coupon"), {"code": "SAVE12", "action": "post"}
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["message"], "A promo code is already applied")
        self.assertEqual(data["status"], "danger")

    def test_apply_promo_code_success(self):
        response = self.client.post(
            reverse("apply_coupon"), {"code": "SAVE12", "action": "post"}
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["message"], "Promo code applied")
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["new_total"], "60.71")
        self.assertEqual(data["discount_amount"], "8.28")
