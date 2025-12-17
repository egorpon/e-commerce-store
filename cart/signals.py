from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import CartItem, Cart
from store.models import Product


@receiver(user_logged_in)
def merge_cart_on_login(sender, user, request, **kwargs):
    guest_session_key = getattr(request, "guest_session_key", None)
    if not guest_session_key:
        return

    guest_cart = Cart.objects.filter(session_key=guest_session_key, user=None).first()

    if not guest_cart:
        return

    user_cart, created = Cart.objects.get_or_create(user=user)

    for guest_item in guest_cart.items.all():
        user_item = user_cart.items.filter(product=guest_item.product).first()
        if user_item:
            user_item.quantity = guest_item.quantity
            user_item.save()
        else:
            guest_item.cart = user_cart
            guest_item.save()

    guest_cart.delete()

