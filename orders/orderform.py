from django import forms
from .models import Order


# -- Create a form for Oder -- #

class OrderForm(forms.ModelForm):
    
    class Meta:
        
        model = Order
        
        # Fields for form 
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']