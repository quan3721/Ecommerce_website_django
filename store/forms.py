from django import forms
from .models import ReviewRating # import ReviewRating model

class ReviewForm(forms.ModelForm):
    
    class Meta:
        
        model = ReviewRating
        
        fields = ['subject', 'review', 'rating']