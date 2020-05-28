import json
from .models import *


def cookieCart(request):

    try:
            cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print(cart)
    total = 0.00
    items = []
    order = {"get_cart_total":0 , "get_cart_items":0, "shipping":False }
    cartItems = order["get_cart_items"]
    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total += product.price * cart[i]['quantity']
            item = {
                "product":{
                    'id':product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
            order['get_cart_total'] = total
            order['get_cart_items'] = cartItems
            order['get_cart_total_paisa'] = total*100
            if product.digital == False:
                order['shipping'] = True
        except:
            pass

        
    return {"order":order,"items":items}