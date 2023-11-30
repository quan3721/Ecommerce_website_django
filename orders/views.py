from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem # import CartItem model
from .orderform import OrderForm # import OrderForm
from .models import Order, Payment, OrderProduct # import Oder, Payment, OrderProduct models
import datetime
import json
from store.models import Product # import Product model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.

def payments(request):
    
    body = json.loads(request.body) # get detail information from json
    # print(body)
    
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID']) # get order
    
    # -- Store transaction details inside Payment model -- #
    payment = Payment(
        user = request.user,
        payment_id =  body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save() # save into Payment model   
    order.payment = payment
    
    # Done Payment, set is_ordered = True
    order.is_ordered = True
    order.save()
    
    
    # Move the cart items to Order Product Model #
    cart_items = CartItem.objects.filter(user=request.user) # cart item
    
    for item in cart_items: # loop for to move item from cart into order product 
        orderproduct = OrderProduct() 
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        # print(item.product) # ATX Jeans
        # print(item.product_id) # 1
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        
        # --  Variation for product -- #
        cart_item = CartItem.objects.get(id=item.id) # get cart item following id
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id) # get order product following id
        orderproduct.variations.set(product_variation)
        orderproduct.save()
    
    
        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    
    
    # Clear cart
    CartItem.objects.filter(user=request.user).delete() # delete cart item following user
    
    
    # Send order received email to customer
    mail_subject = 'Thank your for Your Order!'
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user, # user object
        'order': order,
    })            
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email]) # sending message to email need to verificate
    send_email.send()
    
    
    # Send order number and transaction id to back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)
    
    
    
    # return render(request, 'orders/payments.html',)




# -- Function for Oder with information of Bill -- #
def place_order(request, total=0, quantity=0):
    
    # for total price and tax #
    grand_total = 0
    tax = 0
    
    # current user #
    current_user = request.user 
    
    # if the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user) # get cart items
    cart_count = cart_items.count() # get the number items in cart
    
    if cart_count <= 0: # Not haing any items in cart
        return redirect('store')
    
    # -- calculate tax value and total price -- #
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity) # total price all items
        quantity += cart_item.quantity # the number of items        
    tax = (2 * total)/100 # 2%
    grand_total = total + tax
    
    if request.method == 'POST': 
        form = OrderForm(request.POST)
        if form.is_valid():  # form is valid
            # -- store all the billing information inside Order model -- #
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name'] 
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR') # user ip
            data.save()
            
            # -- Generatate order number -- #
            yr = int(datetime.date.today().strftime('%Y')) # -- year
            dt = int(datetime.date.today().strftime('%d')) # -- date
            mt = int(datetime.date.today().strftime('%m')) # -- month
            d = datetime.date(yr,mt,dt) #20231129 : 2023-11-9
            current_date = d.strftime("%Y%m%d") # time
            order_number = current_date + str(data.id) # create a order number unique
            data.order_number = order_number
            data.save()
            
            
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
                      
            return render(request, 'orders/payments.html', context)
        else:
            print(form.errors) 
    else:
        return redirect('checkout')
    
    


def order_complete(request):
    
    # Get order number and transID from url path #
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    
    try: 
        order = Order.objects.get(order_number=order_number, is_ordered=True) # get order object
        ordered_products = OrderProduct.objects.filter(order_id=order.id) # get order products 
        payment = Payment.objects.get(payment_id=transID) # get payment object
        
        sub_total = 0
        for i in ordered_products: # calculate sub_total
            sub_total += i.product_price * i.quantity 
        
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'sub_total': sub_total
        }
        
        return render(request, 'orders/order_complete.html', context)
    
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
        
        
    
    