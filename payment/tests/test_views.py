from django.test import TestCase

from ..forms import ShippingForm
from ..models import ShippingAddress

from django.urls import reverse
from ..factory import ShippingAddressFactory

from cart.factory import UserFactory


# Create your tests here.
class PaymentViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.shipping_address = ShippingAddressFactory(
            full_name="Benjamin Netanyahu", user=self.user
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
