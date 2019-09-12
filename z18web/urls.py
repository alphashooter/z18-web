"""z18web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import webapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', webapp.views.index),
    path('product/<int:product_id>', webapp.views.product, name='product'),
    path('login', webapp.views.LoginView.as_view(), name='login'),
    path('register', webapp.views.RegisterView.as_view(), name='register'),
    path('cart', webapp.views.CartView.as_view(), name='cart'),
    path('test', webapp.views.TestView.as_view())
]
