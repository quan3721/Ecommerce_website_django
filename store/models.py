from django.db import models
from category.models import Category # import Category model
from django.urls import reverse # import reverse function ( reverse for url )

# Create your models here.

class Product(models.Model):
    
    # -- Field for product name -- #
    product_name = models.CharField(max_length=200, unique=True)
    
    # -- Field for containing url of each products -- #
    slug = models.SlugField(max_length=200, unique=True)
    
    # -- Field for containing descript of products -- #
    description = models.TextField(max_length=500, blank=True)
    
    # -- Field for price of product -- #
    price = models.IntegerField()
    
    # -- Field for containing image of products -- #
    image = models.ImageField(upload_to="photos/products")
    
    # -- Field for containing the number of each products -- #
    stock = models.IntegerField()
    
    # -- Field to check product is available or not -- #
    is_available = models.BooleanField(default=True) # default = True, mặc định : sản phẩm còn hàng
    
    # -- Field for containing the kind of category of products -- #
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # on_delete = models.CASCADE, nếu category chứa product tương ứng thì khi delete category, product cũng bị delete theo
    
    # -- Field for containing the date created product -- #
    created_date = models.DateTimeField(auto_now_add=True)
    
    # -- Field for containing the date modified product -- #
    modified_date = models.DateTimeField(auto_now=True)
    
    # -- Create funtion to get url for each categories in navbar -- # 
    def get_url(self):
        return reverse("product_detail", args=[self.category.slug, self.slug]) # add slug of category and slug of produc, using reverse function 
    
    # -- Display product name -- #
    def __str__(self):
        return self.product_name