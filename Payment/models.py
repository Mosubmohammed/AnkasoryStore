from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ShoppingAddress(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    full_name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    address1=models.CharField(max_length=200)
    address2=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100,null=True, blank=True)
    zipcode=models.CharField(max_length=100)
    country=models.CharField(max_length=100,null=True, blank=True)
    
    class Meta:
        verbose_name_plural="Shopping Address"
    
    def __str__(self):
        return f'Shipping Address - {str(self.id)}'