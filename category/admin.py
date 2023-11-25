from django.contrib import admin
from .models import Category

# Register your models here.

# -- Create a class to edit display Category on admin page -- #
class CategoryAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {'slug': ('category_name',)} # auto fill into slug field when create a new category
    
    list_display = ('category_name', 'slug') # display category name field and slug field


admin.site.register(Category, CategoryAdmin) # register model Category after creating 