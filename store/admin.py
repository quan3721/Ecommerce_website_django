from django.contrib import admin
from .models import Product, Variation # import Product, Variation model

# Register your models here.

# -- Create a class to edit display Product on admin page -- #
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available') # display some fields
    
    prepopulated_fields = {'slug': ('product_name',)} # auto fill into slug field when create a new product

class VariationAdmin(admin.ModelAdmin):
    
    list_display = ('product', 'variation_category', 'variation_value', 'is_active') # display some fields
    
    list_editable = ('is_active',) # edit the is_active field on table admin
    
    list_filter = ('product', 'variation_category', 'variation_value') # create a filter table on admin page

admin.site.register(Product, ProductAdmin) # registor Product model
admin.site.register(Variation, VariationAdmin) # registor Variation model