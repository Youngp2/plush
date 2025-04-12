from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlencode
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from .models import Item, ItemImage
from .cart import Cart

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')


def contact(request):
    return render(request, 'contact.html')

def store(request):
    items = Item.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=ItemImage.objects.filter(is_main=True),
            to_attr='main_image'
        )
    ).all()

    context = {
        'items': items
       }
    return render(request, 'store.html', context)


def details(request, pk):
    item = get_object_or_404(Item, id = pk)
    images = ItemImage.objects.filter(item=item)
    context = {
        'item':item,
        'images':images
    }
    return render(request, 'details.html', context)



# add to cart functions
@require_POST
def add_to_cart(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id = item_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(item.id, quantity)
  
    return redirect('myapp:cart detail')

def cart_detail(request):
    cart = Cart(request)
    context = {
        'cart':cart
    }
    return render(request, 'cart_detail.html', context)


def remove_from_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    # Remove the item from the cart
    cart = Cart(request)
    cart.remove(item.id)
    return redirect('cart_detail')
#checkout views

def checkout(request):
    cart = Cart(request)
    
    # Redirect to cart detail if the cart is empty
    if not cart.cart:
        return redirect('cart_detail')
    
    # Prepare the email body
    subject = 'Order Request'
    body = 'Hello, \n\n I would like to place an order for the following items: \n\n'
    
    for item in cart:
        body += f"- {item['item'].name} (x{item['quantity']}): ${item['total_price']}\n"
    
    body += f'\nTotal Price: ${cart.get_total_price()}\n\nPlease confirm the order.\n\nThank you!'
    
    # Encode the subject and body for the mailto link
    params = {
        'subject': subject,
        'body': body,
    }
    mailto_link = f"mailto:charlottefisherkennel@gmail.com?{urlencode(params)}"
    
    # Redirect to the mailto link
    return render(request, 'checkout.html', {'mailto_link': mailto_link})



