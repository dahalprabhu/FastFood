from django.db import models
from  django.shortcuts import reverse
from django.contrib.auth.models import User, auth 
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here


class Customer(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile_pic.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
    

	def __str__(self):
		return self.name

class Resturants(models.Model):
    name= models.CharField(max_length=100)
    location= models.CharField(max_length=100)
    image= models.ImageField(upload_to='images')
    desc= models.TextField()
    slug= models.SlugField()
  

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        print("!!!!!!!!!!!!!!!! absolute url",self.slug)
        return reverse("hotel", kwargs={
            'slug':self.slug
        })




Categorie_Choices = (
    ('MM','MO:MO'),
    ('CM', 'Chowmein'),
    ('FR','FriedRice')
)
class FoodItems(models.Model):
    name= models.CharField(max_length=100)
    quantity= models.IntegerField(default=0, null=True, blank=True)
    categorie= models.CharField(choices=Categorie_Choices, max_length=3)
    price= models.IntegerField()
    resturant= models.ForeignKey(Resturants, on_delete=models.CASCADE)
    slug= models.SlugField()
    image= models.ImageField(upload_to='foodsimages' , null=True, blank=True)
    def __str__(self):
        return self.name
    
    def get_add_to_cart_url(self):
        print("@@@@@@@@@@@@@@@@@@@@@@@",self.slug)
        return reverse("add-to-cart", kwargs={
            'slug':self.slug
        })
        

    
class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.SET_NULL, blank=True, null=True)
    item= models.ForeignKey(FoodItems, on_delete=models.SET_NULL, blank=True, null=True)
    quantity= models.IntegerField(default=1)
    date_added= models.DateTimeField(auto_now_add=True)
    is_ordered= models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.item.name)
    

    def get_remove_from_cart_url(self):
        print("ppppppppppppppppppppppppp",self)
        return reverse("remove-from-cart", kwargs={'pk':self.pk}) 

    # def get_Checkout_url(self):
    #     return reverse("resturant:checkout", kwargs={'pk':self.pk})
    def get_total_price(self):
        return self.quantity * self.item.price

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    date_ordered=models.DateTimeField(auto_now_add=True)
    is_ordered= models.BooleanField(default=False, null=True, blank=False)
    items= models.ManyToManyField(OrderItem, related_name='order')
    
    
    def __str__(self):
        return str(self.user)



class ShippingAddress(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phoneno= models.CharField(max_length=50, null=True, blank=True)  
    order= models.ForeignKey(Order, on_delete=models.CASCADE)
    address= models.CharField(max_length=50)
    datetime= models.DateTimeField()

    def __str__(self):
        return str(self.user) 







