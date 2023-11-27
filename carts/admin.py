from django.contrib import admin
from .models import Cart, CartItem # import Cart model and CartItem model

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    
    list_display = ('cart_id', 'date_added') # display some fields on admin page

   
class CartItemAdmin(admin.ModelAdmin):
    
    list_display = ('product', 'cart', 'quantity', 'is_active') 
    
admin.site.register(Cart, CartAdmin) # register Cart model

admin.site.register(CartItem, CartItemAdmin) # register CartItem model

