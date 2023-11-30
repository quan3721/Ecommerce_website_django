from django.contrib import admin
from .models import Payment, Order, OrderProduct # import Payment, Order, OrderProduct models

# Register your models here.

class OrderProductInline(admin.TabularInline):
    
    model = OrderProduct # OrderProduct model
    
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered') # fields only read
    
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered' ] # display some fields
    
    list_filter = ['status', 'is_ordered']
    
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email'] # search fields
    
    list_per_page = 20 # 
    
    inlines = [OrderProductInline]






admin.site.register(Payment) # register Payment model
admin.site.register(Order, OrderAdmin) # register Order model
admin.site.register(OrderProduct) # register OrderProduct model