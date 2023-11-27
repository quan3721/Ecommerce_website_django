from .models import Cart, CartItem # import Cart and CartItem model
from .views import _cart_id # import _cart_id function

def counter(request):
    
    cart_count = 0 # variable for calculating total items in cart
    
    if 'admin' in request.path: # if path is currently admin, don't show couting iems inside cart
        return {}
    else: # path is not current admin
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request)) # get cart
            cart_items = CartItem.objects.all().filter(cart=cart[:1]) # get cart_items object but just only one
            for cart_item in cart_items:
                cart_count += cart_item.quantity # calculate total items in cart
        except Cart.DoesNotExist: # if Cart object does not exist
            cart_cout = 0
    
    return dict(cart_count=cart_count)