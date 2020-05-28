from django.urls import path
from .views import store,cart,checkout,updateCart,processOrder,prev_order,register,loginUser,logoutUser

urlpatterns = [
    path('', store,name="store"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('updatecart/', updateCart,name="update_cart"),
    path('process_order/',processOrder,name="process_order"),
    path('prev_order/',prev_order, name="prev_order"),
    path('register/',register, name="register"),
    path('login/',loginUser, name="login"),
    path('logout/',logoutUser,name="logout")
]
