# from django.http import HttpResponse
from django.shortcuts import render, redirect
from store.models import Product

# -- Dispplay home page -- #
def home(request):
    # -- Create a variable to contain all products -- #
    products = Product.objects.all().filter(is_available=True) # filter(is_available=True) : chỉ lấy product còn hàng
    
    # -- Create a variable contain variable producs to display on home page -- #
    context = {
        'products': products,
    }
    
    return render(request, 'home.html', context) # render home page