from decimal import Decimal


from cart.factory import ProductFactory
from core.tests_base import BaseTestClass
from promotion.factory import DiscountFactory


# Create your tests here.
class StoreModelTest(BaseTestClass):
    def setUp(self):
        self.product = ProductFactory()
        self.product_2 = ProductFactory()
        self.discount = DiscountFactory()
        self.discount.products.set([self.product])

    def test_product_sell_price(self):
        self.assertEqual(self.product.sell_price, Decimal("10.39"))
        self.assertEqual(self.product_2.sell_price, Decimal("12.99"))

    def test_product_has_discount(self):
        self.assertTrue(self.product.has_discount)
        self.assertFalse(self.product_2.has_discount)

    def test_product_discount_percent(self):
        self.assertEqual(self.product.discount_percent, 20)
        self.assertEqual(self.product_2.discount_percent, 0)
