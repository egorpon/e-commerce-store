from django.test import TestCase
from ..forms import CreateUserForm, UpdateUserForm
from cart.factory import UserFactory


# Create your tests here.
class AccountFormTest(TestCase):
    def setUp(self):
        return super().setUp()

    def test_create_user_form_email_must_be_unique(self):
        user1 = UserFactory(email="user1@gmail.com")

        data = {
            "username": "user2",
            "email": user1.email,
            "password1": "123321Test",
            "password2": "123321Test",
        }

        form = CreateUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["This email has already been used"])

    def test_update_user_cannot_use_foreign_email(self):
        user1 = UserFactory(username="user1", email="user1@gmal.com")
        user2 = UserFactory(username="user2", email="user2@gmal.com")

        data = {"username": "user2_thief", "email": "user1@gmal.com"}

        form = CreateUserForm(data=data, instance=user2)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["This email has already been used"])

    def test_update_user_email_uniqueness_validation(self):
        user = UserFactory(email="test@gmail.com")

        data = {
            "username": "test",
            "email": user.email,
        }

        form = CreateUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["This email has already been used"])

    def test_update_user_can_change_username_withot_email_changing(self):
        user = UserFactory(email="test@gmail.com")

        data = {
            "username": "new_username",
            "email": "test@gmail.com",
        }

        form = UpdateUserForm(data=data, instance=user)
        self.assertTrue(form.is_valid())