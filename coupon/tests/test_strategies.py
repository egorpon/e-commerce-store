from django.test import TestCase
from ..factory import CouponFactory
from ..discount import (
    get_discount_strategy,
    PercentageDiscount,
    FixedDiscount,
    NoDiscount,
)
from decimal import Decimal


# Create your tests here.
class CouponStrategyTest(TestCase):
    def setUp(self):
        self.percent_coupon = CouponFactory()
        self.fixed_coupon = CouponFactory(type="Fixed")

    def test_percent_coupon_get_percent_discount_strategy(self):
        self.assertIsInstance(
            get_discount_strategy(self.percent_coupon), PercentageDiscount
        )

    def test_fixed_coupon_get_fixed_discount_strategy(self):
        self.assertIsInstance(get_discount_strategy(self.fixed_coupon), FixedDiscount)

    def test_percentage_discount_calc(self):
        strategy = get_discount_strategy(self.percent_coupon)
        self.assertEqual(
            strategy.apply_discount(Decimal("48.99")), round(Decimal("43.112"), 2)
        )

    def test_fixed_discount_calc(self):
        strategy = get_discount_strategy(self.fixed_coupon)
        self.assertEqual(strategy.apply_discount(Decimal("48.99")), Decimal("36.99"))

    def test_fixed_discount_bigger_than_cart_total_price(self):
        coupon = CouponFactory(value=500, type="Fixed")
        strategy = get_discount_strategy(coupon)

        self.assertEqual(strategy.apply_discount(Decimal("48.99")), Decimal("0.00"))

    def test_cart_with_no_coupon_has_no_discount(self):
        coupon = None

        self.assertIsInstance(get_discount_strategy(coupon), NoDiscount)
