from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q # import Q

from .models import Product, ReviewRating # import Product and ReviewRating models

from category.models import Category # import Category model

from carts.views import _cart_id # import _cart_id function

from carts.models import CartItem # import CartItem model

from .forms import ReviewForm # import ReviewForm

from django.contrib import messages
 
from orders.models import OrderProduct # import OrderProduct model


# Create your views here.

# -- Display store page -- #
def store(request, category_slug=None):
    
    categories = None 
    products = None 
    
    # --  check slug of category is exist or None -- #
    if category_slug != None: # Display products by category ( Hiển thị sản phẩm theo loại hàng hóa trên Store Page )
        categories = get_object_or_404(Category, slug=category_slug) # -- variable to store all object from Category model
        products = Product.objects.filter(category=categories, is_available=True) # -- variable to store all object from Product model
        
        # -- Pagination ( Phân trang ) -- # ( Create a page for 1 products )
        paginator = Paginator(products, 1) # only one page contain 1 products
        page = request.GET.get('page') # get url page ( it means url/page=? )
        paged_products = paginator.get_page(page) # page for products
        
        product_count = products.count() # the number of kind of products ( số lượng items )
        
    else: # Display all products on store page ( Hiển thị tất cả sản phẩm trên Store Page )
        # -- Create a variable to contain all products -- #
        products = Product.objects.all().filter(is_available=True).order_by('id') # filter(is_available=True) : chỉ lấy product còn hàng
        
        # -- Pagination ( Phân trang ) -- # ( Create a page for 6 products )
        paginator = Paginator(products, 3) # only one page contain 6 products
        page = request.GET.get('page') # get url page ( it means url/page=? )
        paged_products = paginator.get_page(page) # page for products
        
        product_count = products.count() # the number of kind of products ( số lượng items )
        
  
    
    # -- Create a variable contain variable producs to display on home page -- #
    context = {
        'products': paged_products, # Note: page has contained all product objects
        'product_count': product_count,
    }
    
    return render(request, 'store/store.html', context)



# -- function to show detail product -- #
def product_detail(request, category_slug, product_slug):
    
    try:
        # -- create a variable for single product to contain all information following category slug and product slug -- #
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug) # category__slug : to access into Category model inside Product model to get slug field
        # -- check is this product inside cart ? -- # (in_cart = True : it means that cart have this proudct inside, or else)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists() # cart__cart_id : to access into Cart model inside CartItem product to get cart_id

    except Exception as e:
        raise e # -- except the error
    
    
    # -- Check if product has purchased -- # So user can post review this product
    if request.user.is_authenticated:
        try:
            # orderproduct = OrderProduct.objects.filter(user=request.user.id, product_id=single_product.id).exists() # 1
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists() # 2
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None   
        
    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
        
        
    # -- Create a variable contain variable producs to display on product detail page -- #
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
    }
    
    return render(request, "store/product_detail.html", context)


# -- Function for Searching Product -- #
def search(request):
    
    if 'keyword' in request.GET: # check request method has the keyword or not, if True ( nếu có )
        keyword = request.GET['keyword'] # -- variable contain the input keyword ( name = "keyword" )
        if keyword:
            '''
                description__icontains=keyword : look for whole description of products related the keyword
                product_name__icontains=keyword : look for whole name of products related the keyword
                
                using Q() for operator 'Or' |
            '''
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) |  Q(product_name__icontains=keyword)) 
            product_count = products.count() # the number of products found after searching
            
    context = {
        'products': products,
        'product_count': product_count,
    }
    
    
    return render(request, 'store/store.html', context)


# -- Function for submit review and rating product -- #
def submit_review(request, product_id):
    
    url = request.META.get('HTTP_REFERER') # get url
    
    if request.method == "POST":
        try: 
            # -- Update review
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id) # get reviewrating object following user id and product id
            form = ReviewForm(request.POST, instance=reviews) # instance=reviews, to check if review exist, so only update that review, not create a new
            form.save()
            
            messages.success(request, 'Thank you! Your review has been updated')
            return redirect(url)
        
        except ReviewRating.DoesNotExist:
            # -- Create a review
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR') # ip address
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                
                messages.success(request, 'Thank you! Your review has been submitted')
                
                return redirect(url)