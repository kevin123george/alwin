from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# Create your models here.
class Post(models.Model):

    aut = models.CharField(max_length=255 )
    flat_number = models.CharField(max_length=30)  

   
    time = models.CharField(max_length=255 )

    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.aut

class Item(models.Model):
    item_name=models.CharField(max_length=50, primary_key=True)
    price = models.IntegerField(null= True)
    brand = models.CharField(max_length=30)
    def __str__(self):
            return self.item_name


class Quantity(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    qu = models.IntegerField()
    t = models.ForeignKey('Item', on_delete=models.CASCADE)
    flat_number = models.CharField(max_length=30)