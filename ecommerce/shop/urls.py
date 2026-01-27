"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from shop import views
from django.urls import path
app_name='shop'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.CategoryView.as_view(), name="categories"),
    path('products/<int:i>', views.CategoryProducts.as_view(), name="products"),
    path('register/', views.Register.as_view(), name="register"),
    path('userlogin/', views.Userlogin.as_view(), name="userlogin"),
    path('userlogout/', views.Userlogout.as_view(), name="userlogout"),
    path('adminhome', views.AdminHome.as_view(), name="adminhome"),
    path('details/<int:i>', views.ProductDetails.as_view(), name="details"),
    path('addcategories/', views.AddCategories.as_view(), name="addcategories"),
    path('addproducts/', views.AddProducts.as_view(), name="addproducts"),
    path('addstock/<int:i>', views.AddStock.as_view(), name="addstock"),

]