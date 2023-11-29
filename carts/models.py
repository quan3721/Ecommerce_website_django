from django.db import models
from store.models import Product, Variation # import Product and Variation model
from accounts.models import Account # import Account model

# Create your models here.

class Cart(models.Model):
    
    # -- Field for id of cart -- #
    cart_id = models.CharField(max_length=250, blank=True)
    
    # -- Field for date created of cart -- #
    date_added = models.DateField(auto_now_add=True)
    
    # -- Display cart id -- #
    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    
    # -- Field for containing the user account -- #
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    
    # -- Field for containing the products -- #
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # on_delete = models.CASCADE, nếu cart chứa product tương ứng thì khi delete cart, product cũng bị delete theo
    
    # -- Field for conatining the variation of product -- #
    variations = models.ManyToManyField(Variation, blank=True)
    
    # -- Field for containing the products in cart -- #
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    
    # -- Field for quantity of items in cart -- #
    quantity = models.IntegerField()
    
    is_active = models.BooleanField(default=True) # default = False, 
    
    
    # Total price of each products when add more than one quantity #
    def sub_total(self):
        return self.product.price * self.quantity
    
    
    # -- Display product -- #
    def __unicode__(self):
        return self.product
     