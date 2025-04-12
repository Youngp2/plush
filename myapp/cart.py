from decimal import Decimal
from django.conf import settings
from .models import Item

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
    
    def add(self, item_id, quantity=1, update_quantity=False):
        item = Item.objects.get(id=item_id)
        item_id = str(item.id)
        
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 0, 'price': str(item.price)}
        
        if update_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
            
        self.save()

        # Regenerate the session key to refresh the session
        self.session.cycle_key()
        
    def remove(self, item_id):
        item_id = str(item_id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()
            
    def save(self):
        self.session.modified = True
        
    def __iter__(self):
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)
        for item in items:
            self.cart[str(item.id)]['item'] = item
            
        for item in self.cart.values():
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item
            
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session['cart']
        self.save()