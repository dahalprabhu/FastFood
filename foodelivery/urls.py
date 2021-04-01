from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Cart
from django.conf.urls import url
from . import views

from .views import ( ResturantDetailView, add_to_cart, remove_from_cart, Checkout, add_singleitem_to_cart,
    remove_singleitem_to_cart)

urlpatterns = [
    path('', views.Restaurants , name='home'),
    #path('', HomeView2.as_view() , name='home2')
    path('hotels/<slug>/', ResturantDetailView.as_view() , name='hotel'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('cart/', Cart , name='cart'),
    path('remove-from-cart/<pk>/', remove_from_cart, name='remove-from-cart'),

    path('checkout/', Checkout, name='checkout'),
    path('add_singleitem_to_cart/<slug>/',add_singleitem_to_cart , name='add-singleitem-to-cart'),
    path('remove-singleitem-to-cart/<slug>/',remove_singleitem_to_cart , name='remove-singleitem-to-cart'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboardblue/', views.dashboardblue, name='dashboardblue'),
    path('dashboardbajeko/', views.dashboardbajeko, name='dashboardbajeko'),
    path('account/', views.accountSettings, name="account"),
    path('feedback/', views.feedback, name='feedback'),

#####################################################################################
    url(r'^search/$',views.search),
######
    #  path('user/', views.userPage, name="user-page"),

    path('account/', views.accountSettings, name="account"),

    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_complete"),



    #path('checkout/<pk>/', Checkout, name='checkout')
    #path('checkout-complete/')
]