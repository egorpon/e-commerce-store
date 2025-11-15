from decimal import Decimal, ROUND_HALF_UP

from store.models import Product

from copy import deepcopy

from .models import CartItem

from django.db.models import Sum, F, ExpressionWrapper, DecimalField

from django.db.models.functions import Round


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
        self.request = request
        cart = self.session.get("cart")

        if "cart" not in request.session:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, product_quantity):
        if self.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=self.user, product=product, defaults={"quantity": product_quantity}
            )
            if not created:
                cart_item.quantity = product_quantity
                cart_item.save()
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]["quantity"] = product_quantity
        else:
            self.cart[product_id] = {
                "price": str(product.price),
                "quantity": product_quantity,
            }
        self.session["cart"] = self.cart
        self.session.modified = True

    def delete(self, product_id):
        if self.user.is_authenticated:
            cart_item = CartItem.objects.get(user=self.user, product__id=product_id)
            cart_item.delete()
        else:
            product_id = str(product_id)
            if product_id in self.cart:
                del self.cart[product_id]

            self.session.modified = True

    def update(self, product_id, product_quantity):
        if self.user.is_authenticated:
            cart_item = CartItem.objects.get(user=self.user, product__id=product_id)
            cart_item.quantity = product_quantity
            cart_item.save()

        product_id = str(product_id)
        product_quantity = int(product_quantity)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] = product_quantity
        self.session.modified = True

    def __len__(self):
        if self.user.is_authenticated:
            cart = CartItem.objects.filter(user=self.user).aggregate(total_count=Sum("quantity"))
            return cart["total_count"] or 0

        return sum(item["quantity"] for item in self.cart.values())

    def __iter__(self):
        if self.user.is_authenticated:
            all_products = CartItem.objects.filter(user=self.user)

            for item in all_products:
                yield {
                    "product": item.product,
                    "quantity": item.quantity,
                    "total": Decimal(item.product.price) * item.quantity,
                }
        else:
            all_products_ids = self.cart.keys()

            products = Product.objects.filter(id__in=all_products_ids)

            cart = deepcopy(self.cart)

            for product in products:
                cart[str(product.id)]["product"] = product

            for item in cart.values():
                item["total"] = Decimal(item["price"]) * item["quantity"]
                yield item

    def get_total(self):
        if self.user.is_authenticated:
            cart = CartItem.objects.aggregate(
                total=Sum(
                    ExpressionWrapper(
                        F("product__price") * F("quantity"),
                        output_field=DecimalField(max_digits=10, decimal_places=2),
                    )
                )
            )
            if cart["total"] is None:
                return Decimal("0.00")

            return cart["total"].quantize(Decimal("0.01"), rounding = ROUND_HALF_UP)
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def get_item_total(self, product_id):
        if self.user.is_authenticated:
            cart = (
                CartItem.objects.filter(user=self.user, product__id=product_id)
                .annotate(
                    total=ExpressionWrapper(
                        F("product__price") * F("quantity"),
                        output_field=DecimalField(max_digits=10, decimal_places=2),
                    )
                )
                .first()
            )
            return cart.total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) or 0
        item = self.cart[str(product_id)]
        return Decimal(item["price"]) * item["quantity"]


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
