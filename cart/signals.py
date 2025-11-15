from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import CartItem
from store.models import Product


@receiver(user_logged_in)
def merge_cart_on_login(sender, user, request, **kwargs):
    cart = request.session.get("cart", {})

    if not cart:
        return

    for product_id, item in cart.items():
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={"quantity": item["quantity"]},
        )

        if not created:
            cart_item.quantity = item["quantity"]
            cart_item.save()

    del request.session["cart"]
    request.session.modified = True
