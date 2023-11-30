from django.db import models
from accounts.models import Account # import Account model
from store.models import Product, Variation # import Product and Variation model

# Create your models here.

class Payment(models.Model):
    
    # -- Field user 
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    # -- Field payment id 
    payment_id = models.CharField(max_length=100)
    
    # -- Field payment method
    payment_method = models.CharField(max_length=100)
    
    # -- Field amount paid
    amount_paid = models.CharField(max_length=100)
    
    # -- Field status of payment
    status = models.CharField(max_length=100)
    
    # -- Field date created 
    created_at = models.DateTimeField(auto_now_add=True)
    
    # -- show payment id 
    def __str__(self):
        return self.payment_id


class Order(models.Model):
    
    #  -- Status 
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    
    # -- Field user
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    
    # -- Field payment, get from Payment model
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    
    # -- Field oder number
    order_number = models.CharField(max_length=20)
    
    # -- Field contain information about User get from form Billing Address 
    first_name = models.CharField(max_length=50)    
    last_name = models.CharField(max_length=50)   
    phone = models.CharField(max_length=15)    
    email = models.EmailField(max_length=50)    
    address_line_1 = models.CharField(max_length=50)   
    address_line_2 = models.CharField(max_length=50, blank=True)   
    country = models.CharField(max_length=50)   
    state = models.CharField(max_length=50)   
    city = models.CharField(max_length=50) 
    order_note = models.CharField(max_length=100, blank=True)
    
    # -- Field oder total
    order_total = models.FloatField()
    
    # -- Field for tax
    tax = models.FloatField()
    
    # -- Field status of order
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    
    # -- Field ip 
    ip = models.CharField(blank=True, max_length=20)
    
    is_ordered = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)


    # -- Show the full name of customer
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    # -- Show address of customer
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    # -- Display first name of customer
    def __str__(self):
        return self.first_name    


# -- Model containt product for ordering -- #   
class OrderProduct(models.Model):
    
    # -- Field order
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    # -- Field payment
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    
    # -- Field user
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    # -- Field product in oder
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # -- Field variations of product
    variations = models.ManyToManyField(Variation, blank=True)
    
    # -- Field quantity of product
    quantity = models.IntegerField()
    
    # -- Field price
    product_price = models.FloatField()
    
    ordered = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name