from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart
# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        cartData = cookieCart(request)
        
        order = cartData["order"]  

    products = Product.objects.all()
    context = {
        "order": order,
        "products" : products
    }
    return render(request,'store/store.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        cartData = cookieCart(request)
        order = cartData["order"]
        items = cartData["items"]        
    context = {
        "order": order,
        "items": items
    }
    return render(request,'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        if not items:
            return redirect(store)
    else:
        cartData = cookieCart(request)
        order = cartData["order"]
        items = cartData["items"]   
        if not items:
            return redirect(store)     
        
    context = {
        "order": order,
        "items": items
    }
    return render(request,'store/checkout.html',context)    

def prev_order(request):
    if request.user.is_authenticated:
        items = []
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer,completed=True)
        for order in orders:
            items += OrderItem.objects.all().filter(order=order)
    else:
        return redirect(store)
    context = {
        "items":items,
    }
    return render(request,"store/prev_order.html",context)


def updateCart(request):
    print(request.body)
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    print(customer)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,completed=False)
    orderitem, created = OrderItem.objects.get_or_create(product=product,order=order)
    print(orderitem.product)

    if action == "add":
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == "remove":
        orderitem.quantity = (orderitem.quantity - 1)
    elif action == "delete":
        orderitem.quantity = 0
        orderitem.delete()
        
    orderitem.save()
    if orderitem.quantity <= 0:
        orderitem.delete()
    return JsonResponse("Added Success",safe=False)

def processOrder(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()

    
    address = data['shipping']['address']
    city = data['shipping']['city']
    state = data['shipping']['state']
    zipcode = data['shipping']['zipcode']

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,completed=False)
        
    else:
        name = data['form']['name']
        email = data['form']['email']
        cartData = cookieCart(request)
        items = cartData['items']
        
        customer, created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()
        order = Order.objects.create(customer=customer,completed=False)

        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            orderItem = OrderItem.objects.create(product=product,order=order,quantity=item['quantity'])

    cart_total = float(order.get_cart_total)
    total = float(data['form']['total'])
    if total == cart_total:
        print("hello")
        order.completed = True
        order.transaction_id = transaction_id
        order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(customer=customer,order=order,address=address,city=city,state=state,zipcode=zipcode)
        

            
    return JsonResponse("Order Placed", safe=False)