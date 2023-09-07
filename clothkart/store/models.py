from django.db import models

# Create your models here.
from cart.models import Category
from django.urls import reverse
from user.models import User
from django.db.models import Avg, Count
from user.models import User

# Create your models here.

class Supplier(models.Model):
    first_name=models.CharField(max_length=255,null=True)
    last_name=models.CharField(max_length=255,null=True)
    username=models.CharField(max_length=255,null=True)
    email=models.EmailField(null=True)
    phone_number=models.CharField(max_length=10,null=True)
    business_name=models.CharField(max_length=255,null=True)
    address_lin1=models.CharField(max_length=255,null=True)
    address_lin2=models.CharField(max_length=255,null=True)
    city=models.CharField(max_length=255,null=True)
    district=models.CharField(max_length=255,null=True)
    state=models.CharField(max_length=255,null=True)
    pincode=models.CharField(max_length=6,null=True)
    country=models.CharField(max_length=255,null=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)


class Product(models.Model):
    product_name    = models.CharField(max_length=255, unique=True)
    slug            = models.SlugField(max_length=255, unique=True)
    description     = models.TextField(blank=True)
    price           = models.IntegerField(default=0)
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField(default=0)
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True)
    brand           = models.CharField(max_length=255,null=True)
    supplier        = models.ForeignKey(Supplier, on_delete=models.CASCADE,null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_date    = models.DateTimeField(auto_now_add=True,null=True)
    modified_date   = models.DateTimeField(auto_now=True,null=True)
    todays_deal     = models.BooleanField(default=False)
    mrp           = models.FloatField(default=0)
    offer         = models.IntegerField(default=0)
    
    status   = models.BooleanField(default=True)
    

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def wishlist(self,**kwargs):
        if kwargs('request'):
            request = kwargs.pop('request')
            self.user= request.user
        return Wishlist.objects.filter(product=self,user=request.user,wishlist=True)
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True,status=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True,status=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,)
    variation_category = models.CharField(max_length=255,choices=variation_category_choice, blank=True)
    variation_value     = models.CharField(max_length=255,blank=True)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)
    status              = models.BooleanField(default=True)
    objects = VariationManager()
    def __unicode__(self):
        return self.product

    def __str__(self):
        return self.variation_value
    

class About_Product(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE, blank=True)
    category=models.CharField(max_length=255, blank=True)
    value=models.CharField(max_length=255,blank=True)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    review = models.TextField( blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=255, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
        

class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    wishlist        = models.BooleanField(default=False)




class Customer_care(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255,null=True)
    email = models.EmailField()
    phone_number=models.CharField(max_length=10,blank=True)
    subject = models.CharField(max_length=255,blank=True)
    reason = models.TextField(blank=True)
    ticket = models.CharField(max_length=255,null=True)
    is_solve = models.BooleanField(default=False)
    

