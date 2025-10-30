from decimal import Decimal

from store.models import Product

class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if 'cart' not in request.session:

            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, product_quantity):

        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['quantity'] = product_quantity
        else:
            self.cart[product_id] = {'price': str(product.price),
                                     'quantity': product_quantity}
            
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    

    def __iter__(self):
        all_products_ids = self.cart.keys()

        products = Product.objects.filter(id__in=all_products_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] =  product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['quantity']
            yield item

    def get_total(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

d = {"cart" : {
        "1":{
            "price": Decimal(2.99),
            "quantity": 3,
            "product": Product(...),
            "total": 8.97
        },
        "3":{
            "price":Decimal(19.99),
            "quantity": 1,
            "product": Product(...),
            "total": 19.99
        }
    } }