from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.http.request import *
from django.http.response import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *

# Create your views here.


def index(request: HttpRequest):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def product(request: HttpRequest, product_id: int):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return HttpResponseNotFound()
    return render(request, 'product.html', {'product': product})


class LoginView(View):
    def get(self, request: HttpRequest):
        user: User = request.user
        if user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')

    def post(self, request: HttpRequest):
        user: User = request.user
        if user.is_authenticated:
            return redirect('/')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'login.html')
        login(request, user)
        return redirect('/')


class RegisterView(View):
    def get(self, request: HttpRequest):
        user: User = request.user
        if user.is_authenticated:
            return redirect('/')
        return render(request, 'register.html')

    def post(self, request: HttpRequest):
        user: User = request.user
        if user.is_authenticated:
            return redirect('/')
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=username, password=password)
        except:
            return render(request, 'register.html')
        login(request, user)
        return redirect('/')


class CartView(View):
    def get(self, request: HttpRequest):
        pass

    def post(self, request: HttpRequest):
        product = int(request.POST['product'])
        quantity = int(request.POST['quantity'])
        user: User = request.user
        try:
            profile = user.profile
        except User.profile.RelatedObjectDoesNotExist:
            profile = Profile.objects.create(user=user)
        Cart.objects.create(product=Product.objects.get(pk=product), quantity=quantity, profile=profile)
        return redirect('/')


class TestView(View):
    def get(self, request: HttpRequest):
        return render(request, "test.html", {'form': LoginForm()})

    def post(self, request: HttpRequest):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponse(b'error')
        else:
            return HttpResponse(form.cleaned_data['username'])
