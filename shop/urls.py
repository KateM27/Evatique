from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.registerUser, name='signup'),
    path('<int:pk>/', views.productDetail, name='detail'),
    path('cart/', views.addToCart, name='cart'),
    # path('checkout', views.CheckOut, name='checkout'),
    path('place_order/', views.placeOrder, name='place_order')
]
