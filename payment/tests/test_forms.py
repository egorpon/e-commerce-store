from django.test import TestCase

from ..forms import ShippingForm


# Create your tests here.
class PaymentFormTest(TestCase):
    def test_shipping_form_with_valid_data(self):
        data = {
            "full_name": 'Tester Tester',
            "email" : "test@test.com",
            "city": "Kyiv",
            "address1": "Kyiv kyiv",
            "address2": "",
            "state" : "Kyivska",
            "zipcode":"32145",
        }

        form = ShippingForm(data)

        self.assertTrue(form.is_valid())

    def test_shipping_form_required_fields(self):
        data = {
           
        }

        form = ShippingForm(data)

        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
        self.assertIn('required.', str(form.errors['email']))