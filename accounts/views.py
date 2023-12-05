from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegistrationForm, UserForm, UserProfileForm # import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile # import Account, UserProfile model
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from carts.views import _cart_id # import function _cart_id
from carts.models import Cart, CartItem # import Cart and CartItem model
import requests # must install library
from orders.models import Order, OrderProduct # import Order model


# Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']    
            username = email.split("@") # split value from email
            
            # -- Create a new user -- #
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)           
            user.phone_number = phone_number
            user.save()
            
            # -- Create User Profile -- #
            profile = UserProfile()
            profile.user_id = user.id # get user field
            profile.profile_picture = 'default/default-user.png'
            profile.save()
            
            # -- User activation -- #
            current_site = get_current_site(request) # current site
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user, # user object
                'domain': current_site, # domain
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # encoding the user id so that nobody can see the primary key
                'token': default_token_generator.make_token(user),
            })            
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email]) # sending message to email need to verificate
            send_email.send()
            
                                 
            # messages.success(request, 'Thank you for registering us. We have sent you a verification email to your email address. Please verify it.') # a message notify verify account 
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        # variable to conatin all field from RegistrationForm class #
        form = RegistrationForm()
    

    
    # import context on register page #
    context = {
        'form': form,
    }
    
    return render(request, 'accounts/register.html', context)


# -- Functio to login for User -- #
def login(request):
    
    # -- check method of Form -- #
    if request.method == 'POST':
        email = request.POST['email'] # get the value from name='email'
        password = request.POST['password'] # get the value from name='password'
        
        # -- authenticate email and password with backend and check -- #
        user = auth.authenticate(email=email, password=password)
        
        if user is not None: # if user is valid
            
            # try - except block : to check if having item inside cart, so user can keep item into cart after login
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) # get cart 
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists() # check cart_item exist or not exist
                # print(is_cart_item_exists)
                if is_cart_item_exists: # if exsit
                    cart_item_not_user = CartItem.objects.filter(cart=cart) # get cart_item
                    # -- Fetch all item into user just login -- #
                    
                    # -- getting variation of product exist in user cart by cart_id -- #
                    product_variation = [] # list contain variation product
                    for item in cart_item_not_user:
                        variaton = item.variations.all()
                        product_variation.append(list(variaton)) # note: convert query set into list
                    
                        
                    #  -- Get the cart items from the user to access his product variations  --  #    
                    cart_item_user = CartItem.objects.filter(user=user) # get cart_item information following product added into cart            
                    # existing_variations --> database
                    # current variation --> product_variation list
                    # item_id --> database
                    ex_var_list = []
                    id = []
                    for item in cart_item_user:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation)) # add variation to list, note: convert query set into list,
                        id.append(item.id) # add id of item into list     
                    # print(ex_var_list) # check list
                    
                    
                    '''
                        Loop for to check 'item inside cart when user does not login' with 'item inside cart when user logged in'
                        If exist : increase the item quantity
                        It not exist : create a new item for user cart 
                        
                    '''
                    for pr in product_variation: 
                        if pr in ex_var_list: # if ex_var_list has the value pr
                            index = ex_var_list.index(pr)
                            item_id = id[index] # get item id
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1 # increase the cart item quantity
                            item.user = user # get user for item
                            item.save()
                        else: # if not having
                            cart_item = CartItem.objects.filter(cart=cart)
                            # --  Just assign user for item  -- #
                            for item in cart_item: 
                                item.user = user
                                item.save() 
                                                      
            except:
                pass
            
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            # return redirect('home')
            
            
            # -- using requests library to get url -- #
            url = request.META.get('HTTP_REFERER')
            # check out or           
            try: # check out
                query = requests.utils.urlparse(url).query # get query on path url
                print('query -> ', query) # next=/cart/checkout/
                print('------')    
                params = dict(x.split('=') for x in query.split('&'))
                print('params -> ', params ) # {'next': '/cart/checkout/'}
                
                if 'next' in params: 
                    nextPage = params['next']
                    return redirect(nextPage)                
            except: # login
                return redirect('daskboard')
            
            

        else: # if user is invalid
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
        
    return render(request, 'accounts/login.html')



@login_required(login_url = 'login') # you must be logged in, so that you can log out
def logout(request):
    
    auth.logout(request) # log out
    messages.success(request, 'You are logged out.')   
    return redirect('login') # return to login page



# -- Function for verifying account -- #
def activate(request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # conver into primary key of user
        user = Account._default_manager.get(pk=uid) # get user object
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    # -- check -- # 
    if user is not None and default_token_generator.check_token(user, token): # -- if user exist and have token
        user.is_active = True # actiave the user account
        user.save()
        messages.success(request, 'Congratulation! Your accout is activated.')
        return redirect('login') # return login page
    else: # -- if account isnot created and doesnot have token
        messages.error(request, 'Invalid activation link')
        return redirect('register') # return register page
        
    
    # return HttpResponse('oke')
    
    
# -- Function to access daskboard -- #   
@login_required(login_url = 'login') # you must be logged in, so that you can have daskboard
def daskboard(request):
    
    orders = Order.objects.order_by('-created_at').filter(user_id = request.user.id, is_ordered=True)
    order_count = orders.count() # count the number of order object by user
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    
    context = {
        'order_count': order_count,
        'userprofile': userprofile,
    }
    
    return render(request, 'accounts/daskboard.html', context)



# -- Function to get reset Password when forget password form user -- #
def forgotPassword(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email) # get account from email__exact=email
            
            # -- Reset Password accout from email -- #
            current_site = get_current_site(request) # current site
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user, # user object
                'domain': current_site, # domain
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # encoding the user id so that nobody can see the primary key
                'token': default_token_generator.make_token(user),
            })            
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email]) # sending message to email need to verificate
            send_email.send()
            
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
            
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotPassword')
        
    return render(request, 'accounts/forgotPassword.html')


# -- Function to validate the email is exist or not to Reset Password for this account -- #
def resetpassword_validate(request, uidb64, token):
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # conver into primary key of user
        user = Account._default_manager.get(pk=uid) # get user object
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token): # -- if user exist and have token
        request.session['uid'] = uid # save uid on session for reseting Password
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This is has been expired!')
        return redirect('login')
    
    # return HttpResponse('ok')


# -- Function to reset Password for user -- #
def resetPassword(request):
    
    if request.method == 'POST':
        password = request.POST['password'] # get value from name='password'
        confirm_password = request.POST['confirm_password'] # get value from name='confirm_password'
        
        if password == confirm_password: # return True, if password and confirm_password have the same value
            
            uid = request.session.get('uid') # get uid from session
            user = Account.objects.get(pk=uid) # get user object following pk
            user.set_password(password) # set password for account
            user.save()
            
            messages.success(request, 'Password reset successful')
            return redirect('login')
            
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
        
    else:        
        return render(request, 'accounts/resetPassword.html')
  
   
# -- function to show order in Dashboard of user -- # 
@login_required(login_url='login') # -- user must login, then can see user's order
def my_orders(request):
    
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at') # get order object
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'accounts/my_orders.html', context)  


# -- function to edit profile user in Dashboard -- # 
@login_required(login_url='login') # -- user must login, then can edit your profile
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user) # get user profile
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user) # using instance to update, not create a new one
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('edit_profile')
        
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    
    return render(request, 'accounts/edit_profile.html', context)



# -- Function to change Password for user inside Dashboard -- #
@login_required(login_url='login') # -- user must login, then can change password
def change_password(request):
    
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        user = Account.objects.get(username__exact=request.user.username) # get user object
        
        if new_password == confirm_password:
            success = user.check_password(current_password) # checck correct current_password
            # print(success)
            if success: # if true
                user.set_password(new_password)
                user.save()
                
                # auth.logout(request) # reset password then log out
                
                messages.success(request, 'Password updated successfully')
                return redirect('change_password')

            else: # if not correct
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
            
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
            
    return render(request, 'accounts/change_password.html')


# -- Function to show the detail of user's order inside Dashboard -- #
@login_required(login_url='login') # -- user must login, then can see the order detail
def order_detail(request, order_id):
    
    order_detail = OrderProduct.objects.filter(order__order_number=order_id) # get order products following order id (order number)
    order = Order.objects.get(order_number=order_id) # get order object
    
    sub_total = 0
    for i in order_detail:
        sub_total += i.product.price * i.quantity
    
    
    context = {
        'order_detail': order_detail,
        'order': order,
        'sub_total': sub_total,
    }
    
    return render(request, 'accounts/order_detail.html', context)