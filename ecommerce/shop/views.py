from django.shortcuts import render,redirect
from django.views import View
from shop.models import Category
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from shop.models import Product

#all categories
class CategoryView(View):
    def get(self,request):
        c=Category.objects.all()
        context={'categories':c}
        return render(request,'categories.html',context)

#all products under a specific category
class CategoryProducts(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        context={'category':c}
        return render(request,'products.html',context)

from shop.forms import SignupForm
class Register(View):
    def post(self,request):
        print(request.POST)
        print(request.FILES)
        form_instance = SignupForm(request.POST,request.FILES)
        if (form_instance.is_valid()):
            # data = form_instance.cleaned_data
            # b=Book.objects.create(**data)
            # b.save()
            form_instance.save()
            return redirect('shop:categories')
        context = {'form': form_instance}
        return render(request, "register.html",context)

    def get(self,request):
        form_instance = SignupForm()
        context = {'form': form_instance}
        return render(request, "register.html", context)

from shop.forms import LoginForm
class Userlogin(View):
    def post(self,request):
        form_instance=LoginForm(request.POST)
        if(form_instance.is_valid()):
            data=form_instance.cleaned_data
            u=data['username']
            p=data['password']
            user=authenticate(username=u,password=p)
            if user and user.is_superuser == True:
                login(request,user)
                return redirect('shop:adminhome')
            elif user and user.is_superuser == False:
                login(request,user)
                return redirect('shop:categories')
            else:
                messages.error(request,"Invalid user credentials")
                return redirect('shop:userlogin')
        context = {'form': form_instance}
        return render(request, "userlogin.html", context)

    def get(self,request):
        form_instance =LoginForm()
        context = {'form': form_instance}
        return render(request, "userlogin.html",context)

class Userlogout(View):
    def get(self,request):
        logout(request)
        return redirect("shop:userlogin")

class AdminHome(View):
    def get(self,request):
         return render(request,"adminhome.html")

class ProductDetails(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request,"details.html",context)

from shop.forms import CategoryForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
@method_decorator(login_required,name="dispatch")
class AddCategories(View):
    def get(self,request):
        form_instance = CategoryForm()
        context = {'form': form_instance}
        return render(request,"addcategories.html",context)
    def post(self,request):
        print(request.POST)
        print(request.FILES)
        form_instance = CategoryForm(request.POST,request.FILES)
        if (form_instance.is_valid()):
            # data = form_instance.cleaned_data
            # b=Book.objects.create(**data)
            # b.save()
            form_instance.save()
            return redirect('shop:categories')

from shop.forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
@method_decorator(login_required,name="dispatch")
class AddProducts(View):
    def get(self,request):
        form_instance = ProductForm()
        context = {'form': form_instance}
        return render(request,"addproducts.html",context)
    def post(self,request):
        print(request.POST)
        print(request.FILES)
        form_instance = ProductForm(request.POST,request.FILES)
        if (form_instance.is_valid()):
            # data = form_instance.cleaned_data
            # b=Book.objects.create(**data)
            # b.save()
            form_instance.save()
            return redirect('shop:categories')

from shop.forms import StockForm
class AddStock(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        form_instance = StockForm(instance=p)
        context = {'form': form_instance}
        return render(request,'addstock.html',context)
    def post(self,request,i):
        print(request.POST)
        p=Product.objects.get(id=i)
        form_instance = StockForm(request.POST,instance=p)
        if (form_instance.is_valid()):
            form_instance.save()
            return redirect('shop:categories')



