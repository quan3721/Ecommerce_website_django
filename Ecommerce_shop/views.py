# from django.http import HttpResponse
from django.shortcuts import render, redirect
from store.models import Product
from store.models import ReviewRating # import ReviewRating model

# -- Dispplay home page -- #
def home(request):
    # -- Create a variable to contain all products -- #
    products = Product.objects.all().filter(is_available=True).order_by('created_date') # filter(is_available=True) : chỉ lấy product còn hàng
    
    # Get the reviews
    for product in products:     
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    
    # -- Create a variable contain variable producs to display on home page -- #
    context = {
        'products': products,
        'reviews': reviews,
    }
    
    return render(request, 'home.html', context) # render home page