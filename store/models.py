from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=200, null=True)
  email = models.EmailField(max_length=200, null=True)
  
  def __str__(self):
    return self.name

class Product(models.Model):
  name = models.CharField(max_length=200, null=True)
  price = models.DecimalField(max_digits=9, decimal_places=2)
  digital = models.BooleanField(default=False, null=True, blank=True)
  image = models.ImageField(null=True, blank=True)
  
  def __str__(self):
    return self.name
  
  @property
  def image_url(self):
    try:
      url = self.image.url
    except ValueError:
      url = ""
    return url
  
class Order(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
  date_ordered = models.DateTimeField(auto_now_add=True)
  complete = models.BooleanField(default=False, null=True, blank=True)
  transaction_id = models.CharField(max_length=200, null=True, blank=True)
  
  def __str__(self):
    return str(self.id)
  
  @property
  def shipping(self):
    shipping = False
    order_items = self.orderitem_set.all()
    for order in order_items:
      if order.product.digital == False:
        shipping = True
    return shipping
  
  @property
  def cart_total(self):
    order_items = self.orderitem_set.all()
    total = sum([item.total_item_price for item in order_items])
    return total

  @property
  def cart_items(self):
    order_items = self.orderitem_set.all()
    total = sum([item.quantity for item in order_items])
    return total

class OrderItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
  quantity = models.IntegerField(null=True, blank=True, default=0)
  date_added = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.product.name
  
  @property
  def total_item_price(self):
    total = self.product.price * self.quantity
    return total
  
class ShippingAddress(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
  address = models.CharField(max_length=800, null=True, blank=True)
  city = models.CharField(max_length=200, null=True, blank=True)
  state = models.CharField(max_length=200, null=True, blank=True)
  zipcode = models.CharField(max_length=200, null=True, blank=True)
  date_added = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.address