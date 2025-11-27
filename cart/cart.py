from decimal import Decimal, ROUND_HALF_UP

from store.models import Product

from copy import deepcopy

from .models import CartItem

from django.db.models import Sum, F, ExpressionWrapper, DecimalField

from django.db.models.functions import Round


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.user = request.user

        if not self.session.session_key:
            self.session.create()

    def add(self, product, product_quantity):
        if self.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=self.user, product=product, defaults={"quantity": product_quantity}
            )
        else:
            cart_item, created = CartItem.objects.get_or_create(
                session_key=self.session.session_key,
                user=None,
                product=product,
                defaults={"quantity": product_quantity},
            )

        if not created:
            cart_item.quantity = product_quantity
        cart_item.save()

    def delete(self, product_id):
        if self.user.is_authenticated:
            cart_item = CartItem.objects.filter(
                user=self.user, product__id=product_id
            ).first()
            cart_item.delete()
        else:
            cart_item = CartItem.objects.filter(
                session_key=self.session.session_key, product__id=product_id
            ).first()
            cart_item.delete()

    def update(self, product_id, product_quantity):
        if self.user.is_authenticated:
            cart_item = CartItem.objects.filter(
                user=self.user, product__id=product_id
            ).first()
        else:
            cart_item = CartItem.objects.filter(
                session_key=self.session.session_key, product__id=product_id
            ).first()

        if cart_item:
            cart_item.quantity = product_quantity
            cart_item.save()

    def __len__(self):
        if self.user.is_authenticated:
            qs = CartItem.objects.filter(user=self.user)
        else:
            qs = CartItem.objects.filter(session_key=self.session.session_key)
        cart = qs.aggregate(total_count=Sum("quantity"))

        return cart["total_count"] or 0

    def __iter__(self):
        if self.user.is_authenticated:
            all_products = CartItem.objects.filter(user=self.user)
        else:
            all_products = CartItem.objects.filter(session_key=self.session.session_key)
        for item in all_products:
            yield {
                "product": item.product,
                "quantity": item.quantity,
                "total": Decimal(item.product.price) * item.quantity,
            }

    def get_total(self):
        if self.user.is_authenticated:
            qs = CartItem.objects.filter(user=self.user)
        else:
            qs = CartItem.objects.filter(session_key=self.session.session_key)
        cart = qs.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F("product__price") * F("quantity"),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
        )
        if cart["total"] is None:
            return Decimal("0.00")

        return cart["total"].quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_item_total(self, product_id):
        if self.user.is_authenticated:
            qs = CartItem.objects.filter(user=self.user, product__id=product_id)
        else:
            qs = CartItem.objects.filter(
                session_key=self.session.session_key, product__id=product_id
            )
        qs = qs.annotate(
            total=ExpressionWrapper(
                F("product__price") * F("quantity"),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
        cart = qs.first()

        if not cart:
            return Decimal("0.00")
        return cart.total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# d = {
#     "cart": {
#         "1": {
#             "price": Decimal(2.99),
#             "quantity": 3,
#             "product": Product(...),
#             "total": 8.97,
#         },
#         "3": {
#             "price": Decimal(19.99),
#             "quantity": 1,
#             "product": Product(...),
#             "total": 19.99,
#         },
#     }
# }
