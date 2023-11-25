from django.shortcuts import render, get_object_or_404
from .models import Product # import Product model
from category.models import Category # import Category model

# Create your views here.

def store(request, category_slug=None):
    
    categories = None 
    products = None 
    
    # --  check slug of category is exist or None -- #
    if category_slug != None: # if slug of category is exist
        categories = get_object_or_404(Category, slug=category_slug) # -- variable to store all object from Category model
        products = Product.objects.filter(category=categories, is_available=True) # -- variable to store all object from Product model
        product_count = products.count() # the number of kind of products ( số lượng items )
    else:
        # -- Create a variable to contain all products -- #
        products = Product.objects.all().filter(is_available=True) # filter(is_available=True) : chỉ lấy product còn hàng
        
        product_count = products.count() # the number of kind of products ( số lượng items )
        
  
    
    # -- Create a variable contain variable producs to display on home page -- #
    context = {
        'products': products,
        'product_count': product_count,
    }
    
    return render(request, 'store/store.html', context)

# -- function to show detail product -- #
def product_detail(request, category_slug, product_slug):
    
    try:
        # -- create a variable for single product to contain all information following category slug and product slug -- #
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug) # category__slug : to access into Category model to get slug field
    except Exception as e:
        raise e # -- except the error
    
    # -- Create a variable contain variable producs to display on product detail page -- #
    context = {
        'single_product': single_product,
    }
    
    return render(request, "store/product_detail.html", context)