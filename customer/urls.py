"""pet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from customer import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('orderhistory/',views.orderhistory,name='orderhistory'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('checkout/',views.checkout,name='checkout'),
    path('logout/',views.logout,name='logout'),
    path('forgetpassword/',views.forgetpassword,name='forgetpassword'),
    path('changenewpassword/',views.changenewpassword,name='changenewpassword'),
    path('productdetail/',views.productdetail,name='productdetail'),
    path('bookappointment/<int:pk>',views.bookappointment,name='bookappointment'),
    path('gallerypicture/',views.gallerypicture,name='gallerypicture'),
    path('productdetail/<int:pk>',views.productdetail,name='productdetail'),
    path('doctor/',views.doctor,name='doctor'),
    path('doctordetail/<int:pk>',views.doctordetail,name='doctordetail'),
    path('bookap/ ',views.bookap,name='bookap'),
    path('feedback/ ',views.feedback,name='feedback'),
    path('search/ ',views.search,name='search'),
    path('addtocart/<int:pk>',views.addtocart,name='addtocart'),
    path('addtowish/<int:pk>',views.addtowish,name='addtowish'),
#   categories start
    path('c_cat/ ',views.c_food,name='c_cat'),
    path('c_dog/ ',views.c_dog,name='c_dog'),
    path('c_bird/ ',views.c_bird,name='c_bird'),
    path('c_food/ ',views.c_food,name='c_food'),
    path('c_acc/ ',views.c_acc,name='c_acc'),
#   category end
    # path('likephoto/<int:pk>',views.likephoto,name='likephoto'),
    path('delet_cp/<int:pk>',views.delet_cp,name='delet_cp'),
    path('delwish/<int:pk>',views.delwish,name='delwish'),
    path('update_qty/',views.update_qty,name='update_qty'),
    path('cart/',views.cart,name='cart'),
    path('check/',views.check,name='check'),
    path('amount/',views.amount,name='amount'),
    # path('pay/',views.initiate_payment,name='pay'),
    # path('callback/',views.callback,name='callback'),
  

]

