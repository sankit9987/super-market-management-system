from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.utils.translation import gettext_lazy  as _
from django.contrib.auth.base_user import BaseUserManager

class CustomeUserManger(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError(_("Email is required"))
        email = self.normalize_email(email)
        user = self.model(email = email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("super user is "))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("super user is "))
        return self.create_user(email,password,**extra_fields)


stat = (
    ('pending','pending'),
    ('active','active'),
    ('reject','reject'),
)
class User(AbstractUser):
    username = None
    email = models.EmailField('emial address' , unique=True)
    name= models.CharField(max_length=100)
    Address= models.CharField(max_length=100)
    Address2= models.CharField(max_length=100,null=True)
    mobile_no = models.CharField(max_length=12)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    status = models.CharField(max_length=100,choices=stat,null=True)
    job_type = models.CharField(max_length=100,null=True)
    experience = models.CharField(max_length=100,null=True)
    
    is_active = models.BooleanField(default=True)#done
    is_staff = models.BooleanField(default=False)#done
    is_superuser = models.BooleanField(default=False)#done
    is_user = models.BooleanField(default=False)#done
    is_hr = models.BooleanField(default=False)#done
    is_biller = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomeUserManger()

    def __str__(self):
        return self.email

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Profile', max_length=100)
    price = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
stat = (
    ('packed','packed'),
    ('unpacked','unpacked'),
)
class Payment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    expmonth = models.CharField(max_length=100)
    expyear = models.CharField(max_length=100)
    cardnumber = models.CharField(max_length=100)
    cvv = models.CharField(max_length=100)
    status = models.CharField(max_length=100,choices=stat,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)