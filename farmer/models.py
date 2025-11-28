from django.db import models
from accounts.models import Users
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from dealer.models import Bit
from django.utils import timezone


class Product(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    quality = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    

class Message(models.Model):
    user = models.CharField(max_length=20)
    notification = models.TextField()
    product = models.CharField(max_length=20)

class Tracking(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=100)
    delivery_status = models.CharField(max_length=50, default='Pending')
    delivery_date = models.DateField(null=True, blank=True) 

       

class Agreement(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    agree = models.BooleanField(default=False)      



class Paid(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  
    paidfor = models.ForeignKey(Bit, on_delete=models.CASCADE)  
    amount=models.CharField(max_length=100)
    razor_pay_order_id = models.CharField(max_length=100,null=True,blank=True)  
    razor_pay_payment_id = models.CharField(max_length=100,null=True,blank=True) 
    razor_pay_payment_signature = models.CharField(max_length=100,null=True,blank=True)       
    paid=models.BooleanField(default=False)     

