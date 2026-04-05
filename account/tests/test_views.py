from django.test import TestCase
from django.core import mail
from django.urls import reverse
from django.contrib.auth.models import User

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from ..token import email_token_generator

from cart.factory import UserFactory


from payment.models import ShippingAddress
# Create your tests here.


class AccountViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(
            username="tester",
            is_active=True,
        )

    def test_register_user_with_valid_credentials(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "test",
                "email": "test@gmail.com",
                "password1": "123321Test",
                "password2": "123321Test",
            },
        )

        self.assertRedirects(response, reverse("email_verification_sent"))

        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]

        self.assertEqual(email.subject, "Account verification email")
        self.assertEqual(email.to, ["test@gmail.com"])

        user = User.objects.get(username="test")

        expected_uid = urlsafe_base64_encode(force_bytes(user.pk))

        self.assertIn(expected_uid, email.body)

        token = email_token_generator.make_token(user)

        self.assertIn(token, email.body)
        self.assertTrue(email_token_generator.check_token(user, token))

    def test_register_user_with_invalid_credentials_returns_form_errors(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "test",
                "email": "testgmail.com",
                "password1": "123",
                "password2": "123",
            },
        )

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]

        self.assertFalse(form.is_valid())

        self.assertIn("email", form.errors)
        self.assertIn("This password", str(form.errors))

    def test_email_verification_success(self):
        user = UserFactory(username="test", is_active=False)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = email_token_generator.make_token(user)

        response = self.client.get(
            reverse("email_verification", kwargs={"uidb64": uid, "token": token})
        )

        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertRedirects(response, reverse("email_verification_success"))

    def test_email_verification_invalid_uid(self):
        user = UserFactory(username="test", is_active=False)

        invalid_uid = urlsafe_base64_encode(force_bytes(999))
        token = email_token_generator.make_token(user)

        response = self.client.get(
            reverse(
                "email_verification", kwargs={"uidb64": invalid_uid, "token": token}
            )
        )
        user.refresh_from_db()
        self.assertFalse(user.is_active)
        self.assertRedirects(response, reverse("email_verification_failed"))

    def test_email_verification_invalid_token(self):
        user = UserFactory(username="test", is_active=False)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        invalid_token = email_token_generator.make_token(user) + "abc"

        response = self.client.get(
            reverse(
                "email_verification", kwargs={"uidb64": uid, "token": invalid_token}
            )
        )
        user.refresh_from_db()
        self.assertFalse(user.is_active)
        self.assertRedirects(response, reverse("email_verification_failed"))

    def test_login_user_with_valid_credentials(self):
        self.user.set_password("123321Test")
        self.user.save()

        response = self.client.post(
            reverse("login_user"), {"username": "tester", "password": "123321Test"}
        )

        self.assertRedirects(response, reverse("profile_management"))

        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_login_user_with_invalid_credentials(self):
        self.user.set_password("123321Test")
        self.user.save()

        response = self.client.post(
            reverse("login_user"), {"username": "tester", "password": "123"}
        )

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertIn("password", str(form.errors))

    def test_profile_management_access_login_required(self):
        response = self.client.get(reverse("profile_management"))

        self.assertRedirects(
            response, f"{reverse('login_user')}?next={reverse('profile_management')}"
        )

    def test_profile_management_update_success(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("profile_management"),
            {"username": "tester", "email": "user321@gmail.com"},
        )

        self.assertRedirects(response, reverse("profile_management"))

        self.user.refresh_from_db()

        self.assertEqual(self.user.username, "tester")
        self.assertEqual(self.user.email, "user321@gmail.com")

    def test_profile_management_update_failed(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("profile_management"), {"email": "user321gmail.com"}
        )

        self.assertEqual(response.status_code, 200)

        form = response.context["user_form"]
        self.assertFalse(form.is_valid())
        self.assertIn("email", str(form.errors))

    def test_delete_account_flow(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("delete_account"))

        self.assertRedirects(response, reverse("store"))
        user = User.objects.filter(pk=self.user.pk).first()
        self.assertIsNone(user)

    def test_manage_shipping_create_new(self):
        self.client.force_login(self.user)

        data = {
            "full_name": "tester testerovich",
            "email": "test@gmail.com",
            "city": "Praga",
            "address1": "Praga, St. Praga",
        }

        response = self.client.post(reverse("manage_shipping"), data=data)

        self.assertRedirects(response, reverse("manage_shipping"))

        shipping = ShippingAddress.objects.get(user=self.user)

        self.assertEqual(shipping.city, "Praga")

    def test_manage_shipping_create_new(self):
        self.client.force_login(self.user)

        data = {
            "full_name": "tester testerovich",
            "email": "test@gmail.com",
            "city": "Praga",
            "address1": "Praga, St. Praga",
        }

        response = self.client.post(reverse("manage_shipping"), data=data)

        self.assertRedirects(response, reverse("manage_shipping"))

        shipping = ShippingAddress.objects.get(user=self.user)

        self.assertEqual(shipping.city, "Praga")

    def test_manage_shipping_update_existing(self):
        self.client.force_login(self.user)

        existing_address = ShippingAddress.objects.create(
            full_name="tester testerovich",
            email="tester@gmail.com",
            city="Praga",
            address1="Praga St. Praga",
            user=self.user,
        )

        response = self.client.post(
            reverse("manage_shipping"),
            {
                "full_name": "tester testerovich",
                "email": "tester@gmail.com",
                "address1": "Praga St. Praga",
                "city": "New Deli",
            },
        )

        existing_address.refresh_from_db()

        self.assertRedirects(response, reverse("manage_shipping"))

        self.assertEqual(existing_address.city, "New Deli")

    def test_manage_shipping_validation_error(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("manage_shipping"),
            {
                "full_name": "tester testerovich",
                "email": "tester@gmail.com",
                "address1": "Praga St. Praga",
                "city": "",
            },
        )

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertIn("city", form.errors)
