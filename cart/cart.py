from decimal import Decimal, ROUND_HALF_UP

from .models import Cart, CartItem


class CartService:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.user = request.user

        if not self.session.session_key:
            self.session.create()

        self.cart = self._get_existing_cart()

    def _get_existing_cart(self):
        if self.user.is_authenticated:
            return Cart.objects.filter(user=self.user).first()
        else:
            return Cart.objects.filter(session_key=self.session.session_key, user=None).first()

    def _create_cart(self):
        if self.user.is_authenticated:
            return Cart.objects.create(user=self.user)
        else:
            return Cart.objects.create(
                session_key=self.session.session_key, user=None
            )

    def add(self, product, product_quantity):
        if not self.cart:
            self.cart = self._create_cart()
        cart_item, created = CartItem.objects.get_or_create(
            cart=self.cart, product=product, defaults={"quantity": product_quantity}
        )
        if not created:
            cart_item.quantity = product_quantity
        cart_item.save()

    def delete(self, product_id):
        cart_item = CartItem.objects.filter(
            cart=self.cart, product__id=product_id
        ).first()
        cart_item.delete()

    def update(self, product_id, product_quantity):
        cart_item = CartItem.objects.filter(
            cart=self.cart, product__id=product_id
        ).first()

        if cart_item:
            cart_item.quantity = product_quantity
        cart_item.save()

    def __len__(self):
        if not self.cart:
            return 0
        return self.cart.total_quantity

    def __iter__(self):
        if not self.cart:
            return
        all_products = self.cart.items.all()
        for item in all_products:
            yield {
                "product": item.product,
                "quantity": item.quantity,
                "total": item.item_total_price,
            }

    def get_total(self):
        if not self.cart:
            return 0
        return self.cart.total_price

    def get_item_total(self, product_id):
        item = self.cart.items.filter(product__id = product_id).first()

        if not item:
            return Decimal("0.00")
        return item.item_total_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
