from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from .models import Product, Order, OrderItem, ShippingAddress, User, Customer
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
import json
import datetime
from .utils import cart_data, guest_order

# Create your views here.

def store(request):
  data = cart_data(request)
  cart_items = data['cart_items']

  products = Product.objects.all()
  context = {
    'products': products,
    'cart_items': cart_items
  }
  return render(request, 'store/store.html', context)

def cart(request):
  data = cart_data(request)
  cart_items = data['cart_items']
  order = data['order']
  items = data['items'] 

  context = {
    'items': items,
    'order': order,
    'cart_items': cart_items
    }
  return render(request, 'store/cart.html', context)

def checkout(request):
  data = cart_data(request)
  cart_items = data['cart_items']
  order = data['order']
  items = data['items'] 

  context = {
    'items': items,
    'order': order,
    'cart_items': cart_items
    }
  return render(request, 'store/checkout.html', context)

def update_item(request):
  data = json.loads(request.body)
  product_id = data['productId']
  action = data['action']
  customer = request.user.customer
  product = Product.objects.get(id=product_id)
  order, created = Order.objects.get_or_create(customer=customer, complete=False)
  order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

  if action == 'add':
    order_item.quantity += 1
  elif action == 'remove':
    order_item.quantity -= 1
  order_item.save()

  if order_item.quantity <= 0:
    order_item.delete()
  total_items_price = 0
  total_items = order.cart_items
  item_quantity = order_item.quantity
  total_items_price = order_item.quantity * order_item.product.price
  order_total = order.cart_total
  return JsonResponse({'total_items': total_items, 'item_quantity':item_quantity, 'total_items_price': total_items_price, 'order_total': order_total}, safe=False)

def process_order(request):
  transaction_id = datetime.datetime.now().timestamp()
  data = json.loads(request.body)
  
  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)   
  else:
    customer, order = guest_order(request, data)
  
  total = float(data['form']['total'])
  order.transaction_id = transaction_id
  if total == float(order.cart_total):
    order.complete = True
  order.save()
  
  if order.shipping == True:
    ShippingAddress.objects.create(
      customer = customer, 
      order = order, 
      address = data['shipping']['address'],
      city = data['shipping']['city'],
      state = data['shipping']['state'],
      zipcode = data['shipping']['zipcode'],
    ) 
      
  return JsonResponse('payment complete', safe=False)

def login_page(request):
  return render(request, 'store/login.html')

def login_view(request):
  data = json.loads(request.body)
  username=data['username']
  password=data['password']
  print(username)
  user = authenticate(request, username=username, password=password)
  # Check if authentication successful
  if user is not None:
    login(request, user)
    return JsonResponse("Login successful", safe=False)
  else:
    return JsonResponse("Invalid username or password.", safe=False)
  
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("store"))
  
def register(request):
    data = json.loads(request.body)
    name = data["name"]
    username = data["username"]
    email = data["email"]
    password = data["password"]
    confirmation = data["confirmation"]
    
    # Ensure password matches confirmation
    if password != confirmation:
      return JsonResponse("Passwords must match", safe=False)
    # Attempt to create new user
    try:
      user = User.objects.create_user(username, email, password)
      user.save()
      customer = Customer(user=user, name=name, email=email)
      customer.save()
      return JsonResponse("User created", safe=False)
    except IntegrityError:
      return JsonResponse("Username already taken", safe=False)