from django.db import models

from django.db import models
from user.models import User
from store.models import Product, Variation,Supplier

from cart.models import Category




class Payment(models.Model):


    PAYMENT = (
        ('cash_on_delivery', 'cash on delivery'),
        ('Paypal', 'Paypal'),
        ('razorpay', 'razorpay'),
     
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="payment_user",null=True)
    payment_id = models.CharField(max_length=255,null=True,blank=True)
    payment_method = models.CharField(max_length=255, choices=PAYMENT,blank=True)
    amount_paid = models.CharField(max_length=255,blank=True)
    

    status = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # def __str__(self):
    #     return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=255,blank=True)
    first_name = models.CharField(max_length=255,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    phone = models.CharField(max_length=10,blank=True)
    email = models.EmailField(max_length=255,blank=True)
    address_line_1 = models.CharField(max_length=255,blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255,blank=True)
    pincode = models.CharField(max_length=6,blank=True)
    state = models.CharField(max_length=255,blank=True)
    district = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=255,blank=True)
    order_note = models.CharField(max_length=255, blank=True)
    order_total = models.DecimalField(max_digits=65,default=0,decimal_places=2)
    tax = models.DecimalField(max_digits=65,default=0,decimal_places=2)
    status = models.CharField(max_length=255, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=255)
    is_ordered = models.BooleanField(default=False)
    is_completed=models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.first_name

class MainAgent(models.Model):
      
    agent_organization_name=models.CharField(max_length=255,null=True, blank=True)    
    
     

    state=models.CharField(max_length=255,null=True, blank=True)
    district=models.CharField(max_length=255,null=True, blank=True)
    phone_number=models.CharField(max_length=10,null =True)
    email = models.EmailField(max_length=255,null =True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE,null=True)


class CorporateAgent(models.Model):
    agent_organization_name=models.CharField(max_length=255,null=True, blank=True)    
   
    phone_number=models.CharField(max_length=10,null =True)
    

    email = models.EmailField(max_length=255,null =True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state=models.CharField(max_length=255,null=True, blank=True)
    district=models.CharField(max_length=255,null=True, blank=True)
  
    mainagent=models.ForeignKey(MainAgent, on_delete=models.CASCADE,null=True)


   
class OrderProduct(models.Model):

    STATUS_CHOICES = (
        ('New', 'New'),
        ('Cancellation_requested', 'Cancellation_requested'),
        ('Cancelled', 'Cancelled'),
        
    )

    RETURN_CHOICES = (

        ('New', 'New'),
        ('return_requested', 'return_requested'),
        ('return_complete', 'return_complete'),
         ('return_confirmed', 'return_confirmed'),
        ('refund_initiated', 'refund_initiated'),
        ('refunded', 'refunded'),
        
    )
    ADMIN_RETURN_CHOICES = (
         ('New', 'New'),
        ('return_requested', 'return_requested'),
        ('return_confirmed', 'return_confirmed'),

        ('return_complete', 'return_complete'),
        ('refund_initiated', 'refund_initiated'),
        ('refunded', 'refunded'),


        
    ) 
    
    
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField(default=0)
    product_price = models.DecimalField(max_digits=65,default=0,decimal_places=2)
    tax=models.DecimalField(max_digits=65,default=0,decimal_places=2)
    total_price=models.DecimalField(max_digits=65,default=0,decimal_places=2)
    ordered = models.BooleanField(default=False)
    confirm_order=models.BooleanField(default=False)
    cancel_order=models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_cancelled=models.BooleanField(default=False)
    is_shipped=models.BooleanField(default=False)
    shipment_id= models.CharField(max_length=255,null=True, blank=True)
    is_order=models.BooleanField(default=False)
    cancel_status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_track=models.BooleanField(default=False)
    is_sale_assigned=models.BooleanField(default=False)
    return_status = models.CharField(max_length=255, choices=RETURN_CHOICES, default='New')
    admin_return_status = models.CharField(max_length=255, choices=ADMIN_RETURN_CHOICES, default='New')
    expected_delivery_date= models.DateField(null=True)
    main_agent=models.CharField(max_length=255,null=True)
    corporatesub_agent=models.CharField(max_length=255,null=True)
    status_method=models.CharField(max_length=255,null=True)
    is_reached=models.BooleanField(default=False)
    # state = models.CharField(max_length=50,null=True)
    trackID = models.CharField(max_length=255,null=True, blank=True)
    delivered_date=models.DateField(null=True)
    cancel_request_admin= models.CharField(max_length=255,null=True, blank=True)

    
        #     return self.product.product_name



class Shipment(models.Model):
    
    order=models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)

    trackID = models.CharField(max_length=255,null=True, blank=True)
    orderproduct=models.ForeignKey(OrderProduct, on_delete=models.CASCADE,null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    

class Salesman(models.Model):
    salename =models.CharField(blank=True, max_length=255)
    
    age=models.IntegerField(blank=True)
    address=models.TextField(null=True)
    city=models.CharField(max_length=255,null=True, blank=True)
    pincode=models.CharField(max_length=6,null=True, blank=True)
    
    district=models.CharField(max_length=255,null=True, blank=True)
    # new
    corporateagent=models.ForeignKey(CorporateAgent, on_delete=models.CASCADE,null=True)


class SupplierShipment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    order=models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    salesman= models.ForeignKey(Salesman,on_delete=models.CASCADE,null=True,blank=True)
    is_delivered=models.BooleanField(default=False)
    upload_data=models.ImageField(null=True)
    status_method=models.CharField(max_length=255,null=True)
    location_status=models.CharField(max_length=255,null=True)
    created_date = models.DateField(null=True)
    state=models.CharField(max_length=255,null=True, blank=True)
    district=models.CharField(max_length=255,null=True, blank=True)    
    phone_number=models.CharField(max_length=10,null=True)
    main_agent=models.CharField(max_length=255,null=True)
    corporatesub_agent=models.CharField(max_length=255,null=True)    
    delivered_date = models.DateField(null=True)
    orderproduct=models.ForeignKey(OrderProduct, on_delete=models.CASCADE,null=True)
    expected_delivery_date= models.DateField(null=True)
    status=models.CharField(max_length=255,null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    trackID = models.CharField(max_length=255,null=True, blank=True)
    


class State(models.Model):
    state=models.CharField(max_length=255,null=True, blank=True)  

class District(models.Model):
    district=models.CharField(max_length=255,null=True, blank=True)  

RETURN = (
         ('New', 'New'),
        ('return_requested', 'return_requested'),
        ('return_complete', 'return_complete'),
         ('return_confirmed', 'return_confirmed'),
        ('refund_initiated', 'refund_initiated'),
        ('refunded', 'refunded'),   
    ) 


REASON = (
       
        ('Dont_want_the_product_anymore', 'Dont want the product anymore'),
        ('Quality_of_the_product_is_not_as_expected', 'Quality of the product anot as expected'),
        ('Received_wrong_item', 'Received wrong item'),
        ('Dont_like_this_size/fit_of_the_product', 'Dont like this size/fit of the product'),   
        ('Received_broken/damaged_item','Received_broken/damaged item'), 
        ('Product_is_missing_in_the_product','Product is missing in the product'),   


    )
class Return(models.Model):
    order = models.ForeignKey(OrderProduct, on_delete=models.CASCADE,null=True)
    return_id=models.CharField(max_length=255,null=True)
    reason =  models.CharField(max_length=255, choices=REASON,null =True)
    sub_reason= models.CharField(max_length=255,null=True)
    account_no = models.CharField(max_length=255,null=True)
    confirm_account_no = models.CharField(max_length=25,null=True)
    ifscno = models.CharField(max_length=255,null=True)
    account_holder_name= models.CharField(max_length=255,null=True)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=10,null=True)
    email = models.EmailField(max_length=255,null=True)
    address_line_1 = models.CharField(max_length=255,null=True)
    address_line_2 = models.CharField(max_length=255,blank=True)
    country = models.CharField(max_length=255,null=True)
    return_status = models.CharField(max_length=255, choices=RETURN, default='New')
    admin_return_status = models.CharField(max_length=255, choices=RETURN, default='New')
    pincode = models.CharField(max_length=10,null=True)
    state = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=255,null=True)
    district = models.CharField(max_length=255,null=True)
    return_pickup_date = models.DateField(null=True)
    comments=models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

