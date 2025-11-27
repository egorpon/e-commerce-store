from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import CartItem
from store.models import Product


@receiver(user_logged_in)
def merge_cart_on_login(sender, user, request, **kwargs):

    guest_session_key = getattr(request, 'guest_session_key', None)

    if not guest_session_key:
        return

    guest_cart_items = CartItem.objects.filter(
        session_key=guest_session_key, user=None
    )

    if not guest_cart_items.exists():
        return

    for guest_item in guest_cart_items:
        user_item = CartItem.objects.filter(user=user, product=guest_item.product).first()

        if user_item:

            user_item.quantity = guest_item.quantity
            user_item.save()
            
            guest_item.delete()
        else:

            guest_item.user = user
            guest_item.session_key = None
            guest_item.save()

