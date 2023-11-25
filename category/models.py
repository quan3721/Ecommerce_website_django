from django.db import models
from django.urls import reverse # import reverse function ( reverse for url )

# Create your models here.
# -- Create dabase for category with some fields -- #
class Category(models.Model):
    
    # field of name category #
    category_name = models.CharField(max_length=50, unique=True) # unique = True, chỉ một duy nhất
    
    # field name of url for each categories #
    slug = models.SlugField(max_length=100, unique=True) # unique = True, chỉ một duy nhất
    
    # field for show infomation abou catogry #
    description = models.TextField(max_length=255, blank=True)
    
    # field for entering image of category #
    cat_image = models.ImageField(upload_to='photos/categories', blank=True) # upload_to='photos/categories' : path contain the added image
    
    # -- Edit name Category on page admin -- #
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural= 'Categories'
    
    # -- Create funtion to get url for each categories in navbar -- # 
    def get_url(self):
        return reverse('products_by_category', args=[self.slug]) # using reverse function
    
    # -- Display the name category -- #
    def __str__(self):
        return self.category_name