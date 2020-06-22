from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True,blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False)
    image = models.ImageField(null=True,blank=True)
    description = models.CharField(max_length=200,null=True)
    features = models.CharField(max_length=200,null=True)
    tags = models.CharField(max_length=200,null=True)
    category = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name
    
    @property  #lets u access this as an attribute rather than a method
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'images/placeholder.png'
        return url    
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=True,null=True,blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property 
    def get_cart_total(self):
        total = 0
        orderitems = self.orderitem_set.all()
        for item in orderitems:
           total += item.get_total
        return total

    @property
    def get_cart_total_paisa(self):
        total = 0
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            total += item.get_total
        total *= 100
        return total
    
    @property 
    def get_cart_items(self):
        total = 0
        orderitems = self.orderitem_set.all()
        for item in orderitems:
           total += item.quantity
        return total

    @property 
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product.digital == False:
                shipping = True
        return shipping 

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        try:
            total = self.product.price * self.quantity
        except:
            total = 0
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, blank=True, null=True)
    phone = models.IntegerField(default="1234567890",null=True,blank=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class PaymentOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True,default=True)
    payment_id = models.CharField(max_length=255,null=True,default=True)

    def __int__(self):
        return self.order.id



