from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from . views import (homepage, about, store, services, contact,
                     details, checkout, add_to_cart, remove_from_cart, cart_detail)

app_name = "myapp"

urlpatterns = [
    path('', homepage, name ='homepage'),
    path('about/', about, name ='about'),
    path('availible-puppies/', store, name ='availible_puppies'),
    path('services/', services, name ='services'),
    path('contact/', contact, name ='contact'),
     path('details/<uuid:pk>/', details, name = 'details'),
    
    # cart and checkout urls
    path('checkout/', checkout, name='checkout'),
    
    path('cart/', cart_detail, name='cart detail'),
    path('cart/add/<uuid:item_id>/', add_to_cart, name='add to cart'),
    path('cart/remove/<uuid:item_id>/', remove_from_cart, name='remove from cart'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

