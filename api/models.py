from django.db import models
from django_mysql.models import ListTextField
from django.db.models import CharField
from django.contrib.auth.models import AbstractUser
# Create your models here.

class SendMail(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    email =  ListTextField(
        base_field = CharField(max_length=100),
        default = None,
        null = True,
        blank = True,
        size=None,
    )

########### Token-amount-model #####################

class TokenAmountModel(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.CharField(max_length=255, null=True, blank=True)


class EmailFilteringModel(models.Model):
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)   
    category = models.CharField(help_text="1.promotions 2.spam. 3.social", max_length=255, blank=True, null=True)

########################################################################################################################
class User(AbstractUser):
    username = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(unique=True, max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
class ProductMicroServiceModel(models.Model):
    product_name = models.CharField(max_length=255)
    product_cost = models.CharField(max_length=255)

class OrderMicroServiceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductMicroServiceModel, on_delete=models.CASCADE)        