from django.test import TestCase

from ..forms import ShippingForm
from ..models import ShippingAddress, Order, OrderItem

from django.urls import reverse
from ..factory import ShippingAddressFactory

from cart.factory import (
    UserFactory,
    CartFactory,
    CartItemFactory,
    CategoryFactory,
    ProductFactory,
)

from cart.models import Cart

from decimal import Decimal

from django.core import mail

from core.tests_base import BaseTestClass


# Create your tests here.
class PaymentViewTest(BaseTestClass):
    def setUp(self):
        self.user = UserFactory()
        self.shipping_address = ShippingAddressFactory(
            full_name="Benjamin Netanyahu", user=self.user
        )

        self.category = CategoryFactory()
        self.product = ProductFactory(category=self.category)

        self.cart = CartFactory()
        self.cart_item = CartItemFactory(
            cart=self.cart, product=self.product, quantity=1
        )

    def test_checkout_show_saved_user_shipping_address(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("checkout"))

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.initial["full_name"], "Benjamin Netanyahu")

    def test_checkout_anonymous(self):
        response = self.client.get(reverse("checkout"))

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertEqual(form.initial, {})

    def test_payment_success_deletes_user_cart(self):
        self.cart.user = self.user
        self.cart.save()

        self.cart.refresh_from_db()

        self.client.force_login(self.user)

        response = self.client.get(reverse("payment_success"))

        self.assertEqual(response.status_code, 200)
        cart = Cart.objects.filter(user=self.user)
        self.assertFalse(cart.exists())

    def test_payment_success_deletes_guest_cart(self):
        session_key = self.client.session.session_key
        self.cart.session_key = session_key
        self.cart.save()

        self.cart.refresh_from_db()

        response = self.client.get(reverse("payment_success"))

        self.assertEqual(response.status_code, 200)
        cart = Cart.objects.filter(session_key=session_key)
        self.assertFalse(cart.exists())

    def test_complete_order_authorized_user_flow(self):
        self.client.force_login(self.user)
        self.cart.user = self.user

        self.cart.save()
        self.cart.refresh_from_db()

        data = {
            "action": "post",
            "name": "Benjamin",
            "email": "test@test.com",
            "address1": "Main St 1",
            "city": "Tel Aviv",
            "zipcode": "12345",
        }

        response = self.client.post(reverse("complete_order"), data=data)

        self.assertEqual(response.status_code, 200)


        order = Order.objects.filter(full_name="Benjamin", user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.amount_paid, Decimal("12.99"))

        expected_address = 'Main St 1\nTel Aviv\n12345'
        self.assertEqual(order.shipping_address, expected_address)

        order_item = OrderItem.objects.filter(order=order).first()
        self.assertIsNotNone(order_item)
        self.assertEqual(order_item.product, self.product)

        self.assertEqual(response.json()["success"], True)

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        self.assertIn("Order", email.subject)
        self.assertIn("Total paid", email.body)

    def test_complete_order_unauthorized_user_flow(self):
        session_key = self.client.session.session_key
        self.cart.session_key = session_key
        self.cart.save()

        data = {
            "action": "post",
            "name": "Benjamin",
            "email": "test@test.com",
            "address1": "Main St 1",
            "city": "Tel Aviv",
            "zipcode": "12345",
        }

        response = self.client.post(reverse("complete_order"), data=data)

        self.assertEqual(response.status_code, 200)


        order = Order.objects.filter(full_name="Benjamin", user=None).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.amount_paid, Decimal("12.99"))

        expected_address = 'Main St 1\nTel Aviv\n12345'
        self.assertEqual(order.shipping_address, expected_address)

        order_item = OrderItem.objects.filter(order=order).first()
        self.assertIsNotNone(order_item)
        self.assertEqual(order_item.product, self.product)

        self.assertEqual(response.json()["success"], True)

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        self.assertIn("Order", email.subject)
        self.assertIn("Total paid", email.body)


