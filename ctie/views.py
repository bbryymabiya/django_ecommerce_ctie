from django.shortcuts import render, redirect
from .models import *
from django.views.generic import View, TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from .decorators import unauthenticated_user
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, CustomerRegistrationForm
from django.http import JsonResponse
import json
import datetime
from django.urls import reverse_lazy


# Create your views here.

def index(request):
    if 'q' in request.GET:
        q = request.GET['q']
        products = Product.objects.filter(search_by__icontains=q)
    else:
        products = Product.objects.all()

    if request.user.is_authenticated:
        if request.user.customer:
            customer = request.user.customer
        else:
            customer = Customer.objects.create_customer(user=request.user, name=request.user.get('username'), email=request.user.get('email'))
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'ctie/index.html', context)


def productDetail(request, id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    product = Product.objects.get(id=id)
    context = {'product': product, 'cartItems':cartItems}
    return render(request, 'ctie/product-detail.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'ctie/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    context = {'order': order, 'cartItems': cartItems}
    return render(request, 'ctie/checkout.html', context)


# def registerPage(request):
#     form = CreateUserForm()
#
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, 'Account was created for ' + username)
#
#             return redirect('login')
#
#     context = {'form': form}
#     return render(request, 'ctie/register.html', context)


# @unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username Or Password is incorrect')

    context = {}
    return render(request, 'ctie/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def userProfile(request):
    customer = request.user.customer
    order = Order.objects.filter(complete=True)
    context = {'customer': customer, 'orders': order}
    return render(request, 'ctie/profile.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False,)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    elif action == 'delete-item':
        orderItem.quantity = (orderItem.quantity * 0)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        Orders_made.objects.create(
            customer=customer,
            order=order,
            fname=data['form']['fname'],
            lname=data['form']['lname'],
            email=data['form']['email'],
            address=data['form']['address'],
            number=data['form']['number'],
            agent=data['form']['agent'],
            shipby=data['form']['shipby'],

        )

    return JsonResponse('Order Submitted', safe=False)


class CustomerRegistrationView(CreateView):
    template_name = 'register.html'
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username=username, email=email, password=password)
        form.instance.user = user

        return super().form_valid(form)
