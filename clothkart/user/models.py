from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
       
        )

        user.set_password(password)
        user.roll="customer"
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.roll="admin"
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):

    ROLE = (
        ('admin', 'admin'),
        ('staff', 'staff'),
        ('supplier', 'supplier'),
        ('customer', 'customer'),
        ('customer_care', 'customer_care'),
        ('mainagent', 'mainagent'),
        ('subagent', 'subagent'),
        ('salesman', 'salesman'),
    )
    first_name      = models.CharField(max_length=255,null=True)
    last_name       = models.CharField(max_length=255,null=True)
    username        = models.CharField(max_length=255,null=True, unique=True)
    email           = models.EmailField(unique=True)
    phone_number    = models.CharField(max_length=255)
    roll = models.CharField(max_length=255, choices=ROLE, null=True)
    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)
    is_superadmin        = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=255)
    address_line_2 = models.CharField(blank=True, max_length=255)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile',default="images/avatars/avatar3.jpg")
    city = models.CharField(blank=True, max_length=255)
    state = models.CharField(blank=True, max_length=255)
    country = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
