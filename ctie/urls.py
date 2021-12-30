from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('product-detail/<int:id>', views.productDetail, name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', CustomerRegistrationView.as_view(), name='register'),
    # path('register/', views.registerPage, name='register'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('profile/', views.userProfile, name='profile'),
    path('category/', views.category, name='category'),

]