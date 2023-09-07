from django.db import models
from store.models import Product
from user.models import User
from store.models import Customer_care







class customer_Solution(models.Model):
    customer=models.ForeignKey(Customer_care,on_delete=models.CASCADE,null=True)
    subject=models.CharField(max_length=255,null=True)
    solutiom=models.TextField(null=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)   
 
