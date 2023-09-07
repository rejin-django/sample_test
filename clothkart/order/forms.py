from django import forms
from .models import Order,Salesman




class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'pincode','phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note','district']

class SalesmanForm(forms.ModelForm):
    class Meta:
        model=Salesman
        fields = ('salename','age','address','city','district','pincode')

# class AssignForm(forms.ModelForm):
#     class Meta:
#         model=Assignto
#         fields = ['salesman','product']