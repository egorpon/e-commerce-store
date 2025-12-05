from .cart import CartService

def cart(request):
    return {"cart": CartService(request)}