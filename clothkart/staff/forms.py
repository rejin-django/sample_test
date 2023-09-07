from store.models import Product,ProductGallery,Variation,Supplier
from django import forms
from cart.models import Category
from order.models import SupplierShipment,SupplierShipment,CorporateAgent,MainAgent
from .models import customer_Solution

from store.models import About_Product


class Product_Form(forms.ModelForm):  
    class Meta:  
        model = Product
        prepopulated_fields = {'slug': ('product_name',)}
        fields = ['product_name','slug','description','price','images','stock','category','supplier','brand','mrp',]


class Category_Form(forms.ModelForm):  
    class Meta:  
        model = Category
        prepopulated_fields = {'slug': ('category_name',)}
        fields = ['category_name','slug','description','cat_image']


class Variation_Form(forms.ModelForm):  
    class Meta:  
        model = Variation
        
        fields = ['product','variation_category','variation_value']


class Product_gallery_Form(forms.ModelForm):  
    class Meta:  
        model = ProductGallery
        
        fields = ['product','image']

class Supplier_Form(forms.ModelForm):  
    class Meta:  
        model = Supplier
        
        fields = '__all__'

class Corporate_Form(forms.ModelForm):  
    class Meta:  
        model = CorporateAgent
        
        fields = ['agent_organization_name','phone_number','email']

class MainAgent_Form(forms.ModelForm):  
    class Meta:  
        model = MainAgent
        
        fields = ['agent_organization_name','phone_number','email']

# class CorporateShipmentForm(forms.ModelForm):  
#     class Meta:  
#         model = CorporateShipment
        
#         fields =  ['source_address','destination_address','phone_number','sending_date','arrival_date','corporateID']

class SupplierShipmentForm(forms.ModelForm):  
    class Meta:  
        model = SupplierShipment
        
        fields =  ['main_agent','expected_delivery_date','created_date','state','district','location_status']

class About_Product_Form(forms.ModelForm):  
    class Meta:  
        model = About_Product
        
        fields = ['product','category','value']




class Customer_solution_Form(forms.ModelForm):  
    class Meta:  
        model = customer_Solution
        
        fields = ['subject','solutiom']
