from decimal import Decimal

from cart.factory import CategoryFactory, ProductFactory
from core.tests_base import BaseTestClass

from ..discount import get_discounted_price
from ..factory import DiscountFactory


# Create your tests here.
class PromotionDiscountTest(BaseTestClass):
    def setUp(self):
        self.category = CategoryFactory()
        self.product = ProductFactory(category=self.category)

    def test_product_without_discount_get_original_price(self):
        price = get_discounted_price(self.product)

        self.assertEqual(price, self.product.price)

    def test_product_with_discount_get_discounted_price(self):
        discount = DiscountFactory()
        discount.products.set([self.product])

        price = get_discounted_price(self.product)

        self.assertEqual(price, Decimal("10.39"))

    def test_product_with_category_discount_get_discounted_price(self):
        discount = DiscountFactory()
        discount.categories.set([self.category])
        price = get_discounted_price(self.product)

        self.assertEqual(price, Decimal("10.39"))
