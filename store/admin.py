from django.contrib import admin
from .models import Product # import Product model

# Register your models here.

# -- Create a class to edit display Product on admin page -- #
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available') # display some fields
    
    prepopulated_fields = {'slug': ('product_name',)} # auto fill into slug field when create a new product

admin.site.register(Product, ProductAdmin) # registor Product model