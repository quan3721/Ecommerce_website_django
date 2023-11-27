from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from store.models import Product # import Product model
from .models import Cart, CartItem # import Cart, CartItem model
from django.core.exceptions import ObjectDoesNotExist # import ObjectDoesNotExist
from store.models import Variation # import Variation model


# Create your views here.


# -- Private function to get cart it following session key -- # ( note : private function have ' _ ' before name function )
def _cart_id(request):
    
    cart = request.session.session_key # get cart id
    if not cart: # if not having session key
        cart = request.session.create() # create a new 
    return cart


# -- function to add product into cart -- #
def add_cart(request, product_id):
    
    # -- get information about product following id (pk) -- #
    product = Product.objects.get(id=product_id)
    
    product_variation = [] # list contain variation product
    
    if request.method == "POST": # check the method of form 
        # get the key and value from form #
        for item in request.POST: 
            key = item
            value = request.POST[key]
            # print(key, value)
            
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value) # get variation ( filter with __iexact: không phân biệt chữ in hoa vs chũ thường )
                # print(variation)
                product_variation.append(variation) # -- add the value variation into list
            except:
                pass
            
        # # -- Color of product -- #
        # # color = request.GET['color'] # name="color", get value from url by GET request
        # color = request.POST['color'] # name="color"
        # # -- Size of product -- #
        # # size = request.GET['size'] # name="size", get value from url by GET request
        # size = request.POST['size'] # name="size"
        # print(color, size)


    # try - except block to get cart #
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist: 
        # Create a new cart #
        cart = Cart.objects.create( 
            cart_id = _cart_id(request)
        )    
        cart.save() # save cart
    
    # -- try - except block to get cart item (its means items inside cart) -- # Convert try-except into if-else
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists() # check cart_item exist or not exist
    if is_cart_item_exists:
    # try:
        cart_item = CartItem.objects.filter(product=product, cart=cart) # get cart_item information following product added into cart
        
        # existing_variations --> database
        # current variation --> product_variation list
        # item_id --> database
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation)) # add variation to list, note: convert query set into list,
            id.append(item.id) # add id of item into list     
        print(ex_var_list) # check list
        
        if product_variation in ex_var_list: # increase the cart item quantity
            # return HttpResponse('true')
                        
            # -- Get item id -- #
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1 # increase quantity of this item
            item.save()
        else:
            # return HttpResponse('false')
            item = CartItem.objects.create(product=product, quantity=1, cart=cart) # create a new object into CartItem
            # create a new cart item
            if len(product_variation) > 0:
                item.variations.clear() # clear variation init    
                item.variations.add(*product_variation) # * make sure query add product_variation, this code its means product is exist but user want to add new variation for it              
            item.save()
            
    # except CartItem.DoesNotExist:
    else: # cart item not exist    
        # -- Create new object cart item   
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        # -- check if variation has previous value, remove its and add product with variation  
        if len(product_variation) > 0:
            cart_item.variations.clear() # clear variation init
            cart_item.variations.add(*product_variation)  # add product with variation(size, color) in variations field                   
        cart_item.save() # save cart item
    
    # return HttpResponse(cart_item.quantity)
    # exit()
    return redirect('cart') # go to cart page
 

# -- Function to decrease Item from Cart -- #
def remove_cart(request, product_id, cart_item_id):
    
    cart = Cart.objects.get(cart_id=_cart_id(request)) # get cart followiing cart_id
    
    # Using get_object_or_404 to get obejct if it present or return error 404 #
    product = get_object_or_404(Product, id=product_id)
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) # get cart_item

        if cart_item.quantity > 1: # descrease quantity Item on Cart Page
            cart_item.quantity -= 1
            cart_item.save()
        else:  # if quantity of item = 1 --> delete item
            cart_item.delete()
    except:
        pass
    
    return redirect('cart') # go back to Cart Page


# -- Function to Delete Item From Cart -- #
def remove_cart_item(request, product_id, cart_item_id):
    
    cart = Cart.objects.get(cart_id=_cart_id(request)) # get cart
    
    product = get_object_or_404(Product, id=product_id) # get product
  
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) # get cart item
    cart_item.delete() # delete item in Cart
    return redirect('cart')

     
# -- Display cart page -- #
def cart(request, total=0, quantity=0, cart_items=None):
    
    try: # get items added into cart page       
        tax = 0
        grand_total = 0
        # -- get cart objects following cart_id -- #
        cart = Cart.objects.get(cart_id=_cart_id(request)) # using function _cart_id to get cart_id

        cart_items = CartItem.objects.filter(cart=cart, is_active=True) # get cart_item information following cart field and is_active field
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) # total price all items
            quantity += cart_item.quantity # the number of items
            
        # -- tax -- #
        tax = (2 * total)/100 # 2%
        grand_total = total + tax
        
    except ObjectDoesNotExist:
        pass # just ignore ( bỏ qua )
    
    # Display information on cart page #
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    
    return render(request, 'store/cart.html', context)