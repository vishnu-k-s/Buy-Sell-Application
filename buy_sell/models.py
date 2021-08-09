from django.db import models


#Model for user registration
class NewUser(models.Model):
    username = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    phonenumber = models.CharField(max_length=10)
    password = models.CharField(max_length=150)
    #confirmpassword = models.CharField(max_length=150)

    def __str__(self):
        return self.name
        

#Model for category details
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


#Model for products
class Product(models.Model):
    ownerusername = models.CharField(max_length=100, null=True, blank=True)
    owneremail = models.EmailField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=500, default='', null=True, blank=True)
    image  = models.ImageField(upload_to='images/productimages/')
    status = models.CharField(max_length=100, default='sale')

#Model for purchased products
class MyPurchases(models.Model):
    customeremail = models.EmailField(max_length=150, default='')
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    #category = models.CharField(max_length=50,default='', null=True, blank=True)
    #description = models.CharField(max_length=500, default='', null=True, blank=True)
    image  = models.ImageField(upload_to='images/productimages/', null=True, blank=True)
