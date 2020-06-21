from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import CreateUserForm
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart
from .filters import ProductFilter

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        items_dictionary = {}
        # for item in items:
        #     items_dictionary.update( {item.product : item.quantity} )
        # print(items_dictionary)
    else:
        cartData = cookieCart(request)
        items_dictionary={}
        order = cartData["order"] 
        items = cartData["items"]

    products = Product.objects.all()
    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs
    context = {
        "myFilter":myFilter,
        "items":items_dictionary,
        "order": order,
        "products" : products
    }
    return render(request,'store/store.html',context)


def home(request):
    context = {}
    return render(request,"store/home.html",context)
def product(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
    else:
        cartData = cookieCart(request)
        order = cartData["order"] 

    product_id = request.GET.get("id")
    product = Product.objects.get(id=product_id)
    context = {
        "order":order,
        "product":product,
    }
    return render(request,"store/product.html",context)

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
        customer_details = Customer.objects.get(name=customer)
        if not items:
            return redirect(store)
    else:
        customer_details = "Guest User"
        cartData = cookieCart(request)
        order = cartData["order"]
        items = cartData["items"]   
        if not items:
            return redirect(store)     
        
    context = {
        "customer":customer_details,
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
        "orders":orders,
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

    razorpay_id = data['razorpay']['razorpay_payment_id']
    
    address = data['shipping']['address']
    city = data['shipping']['city']
    state = data['shipping']['state']
    zipcode = data['shipping']['zipcode']
    phone = data['shipping']['phone']

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
        ShippingAddress.objects.create(customer=customer,order=order,address=address,city=city,state=state,zipcode=zipcode,phone=phone)

    # Saving payment details to PaymentOrder model

    PaymentOrder.objects.create(customer=customer,order=order,payment_id=razorpay_id)  

            
    return JsonResponse("Order Placed", safe=False)

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        print("in")
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print("Valid")
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user = User.objects.get(username=username)
            Customer.objects.create(user=user,name=username,email=email)
            
            messages.success(request,"Account was created for " + username)
            return redirect("login")
    context = {"form":form}
    return render(request,"store/register.html",context)

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        user = authenticate(request, username=username,password=password)
        if user is not None:
            print("in2")
            login(request, user)
            return redirect("store")
        else:
            messages.info(request,"Username or Password is incorrect")

    context = {}
    return render(request,"store/login.html",context)

def logoutUser(request):
    logout(request)
    return redirect("login")