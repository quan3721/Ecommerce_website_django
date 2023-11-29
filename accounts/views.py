from django.shortcuts import render, redirect
from .forms import RegistrationForm # import RegistrationForm class
from .models import Account # import Account model
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from carts.views import _cart_id # import function _cart_id
from carts.models import Cart, CartItem # import Cart and CartItem model
import requests # must install library

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
    
    
    return render(request, 'accounts/daskboard.html')



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
  
    
     