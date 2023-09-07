from .models import Product
from .models import ReviewRating
from django import forms



class Product_Form(forms.ModelForm):  
    class Meta:  
        model = Product
        prepopulated_fields = {'slug': ('product_name',)}
        fields = ['product_name','slug','description','price','images','stock','category']





class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']