from django.db import models
from category.models import Category # import Category model
from django.urls import reverse # import reverse function ( reverse for url )
from accounts.models import Account # import Account model
from django.db.models import Avg, Count

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
    
    # -- average rating review -- #
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    # -- Count Rating Review -- #
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    

# -- Create a class For managing size and color -- #
class VariationManager(models.Manager):
    
    # -- For color -- #
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    
    # -- For size -- #
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)



variation_category_choice = (
    ('color', 'color'), # the first "color" is the value, and the second "color" is the label (see in HTML)
    ('size', 'size'), # the first "size" is the value, and the second "size" is the label (see in HTML)
)


# Product Variation Model #
class Variation(models.Model):
    
    # -- Field for containing all information about product -- #
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # on_delete = models.CASCADE, nếu product bị xóa thì variation product cũng bị delete theo
    
    # -- Field for containing variation of product -- #
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    
    # -- Field for containing value of variation product -- #
    variation_value = models.CharField(max_length=200)
    
     # -- Field to check variation product is active or not -- #
    is_active = models.BooleanField(default=True) # default = True, mặc định : variation còn hàng
    
    # -- Field for containing the date created variation product -- #
    created_date = models.DateTimeField(auto_now=True)
    
    # -- Manage Field in Model -- #
    objects = VariationManager()
    
    # -- Display product -- #
    def __str__(self):
        return self.variation_value
    
    

class ReviewRating(models.Model):
    
    # -- Field contain porduct need to review and rating -- #
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # -- Field contain the user review and raing product -- #
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    # -- Field contain the subject of review and rating -- #
    subject = models.CharField(max_length=100, blank=True)
    
    # -- Field contain the content of review -- #
    review = models.TextField(max_length=500, blank=True)
    
    # -- Field contain the rating of product -- #
    rating = models.FloatField()
    
    ip = models.CharField(max_length=20, blank=True)
    
    status = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    # -- Display the content of subject -- #
    def __str__(self):
        return self.subject
    
    

# -- Product Gallery Model -- #
class ProductGallery(models.Model):
    
    # -- Field contain product -- #
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    
    # -- Field contain more images for each products -- #
    image = models.ImageField(upload_to='store/products', max_length=255)
    
    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'