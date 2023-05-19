import json
from .models import Product, Order, Customer, OrderItem

def cookie_cart(request):
  try:
    cart = json.loads(request.COOKIES['cart'])
  except KeyError:
    cart = {}
  items = []
  order = {'cart_total': 0, 'cart_items': 0, 'shipping': False}
  cart_items = order['cart_items']
  for i in cart:
    try:
      cart_items += cart[i]['quantity']
      product = Product.objects.get(id=i)
      total = (product.price * cart[i]['quantity'])
      order['cart_total'] += total
      order['cart_items'] += cart[i]['quantity']
      item = {
        'product': {
          'id': product.id,
          'name': product.name,
          'price': product.price,
          'image_url': product.image_url,
        },
        'quantity': cart[i]['quantity'],
        'total_item_price': total,
      }
      items.append(item)
      if product.digital == False:
        order['shipping'] = True
    except:
      pass
  return {'cart_items': cart_items, 'order': order, 'items': items}

def cart_data(request):
  if request.user.is_authenticated:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
      items = order.orderitem_set.all()
      cart_items = order.cart_items
  else:
    cookie_data = cookie_cart(request)
    cart_items = cookie_data['cart_items']
    order = cookie_data['order']
    items = cookie_data['items'] 
  return {'cart_items': cart_items, 'order': order, 'items': items}

def guest_order(request, data):
  name = data['form']['name']
  email = data['form']['email']
  
  cookie_data = cookie_cart(request)
  items = cookie_data['items']
  
  customer, created = Customer.objects.get_or_create(email=email)
  customer.name = name
  customer.save()
  
  order = Order.objects.create(customer=customer, complete=False)
  
  for item in items:
    product = Product.objects.get(id=item['product']['id'])
    order_item = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])

  return customer, order