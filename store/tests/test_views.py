from django.urls import reverse

from cart.factory import CategoryFactory, ProductFactory
from core.tests_base import BaseTestClass


# Create your tests here.
class StoreViewTest(BaseTestClass):
    def setUp(self):
        self.category = CategoryFactory()
        self.product_1 = ProductFactory(category=self.category)
        self.product_2 = ProductFactory(category=self.category)

    def test_store_view_returns_all_products(self):
        response = self.client.get(reverse("store"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["all_products"],
            [self.product_1, self.product_2],
            ordered=False,
        )

    def test_list_categories_returns_products_filtered_by_category(self):

        response = self.client.get(
            reverse("list_category", kwargs={"category_slug": self.category.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["category"], self.category)
        self.assertQuerySetEqual(
            response.context["products"],
            [self.product_1, self.product_2],
            ordered=False,
        )

    def test_product_info_returns_exact_product(self):

        response = self.client.get(
            reverse("product_info", kwargs={"product_slug": self.product_1.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["product"], self.product_1)
