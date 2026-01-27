from django.shortcuts import render,redirect
from django.utils.decorators import decorator_from_middleware
from django.views import View
from shop.models import Product
from cart.models import Cart
import uuid

class AddtoCart(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)
            c.quantity+=1
            c.save()
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)
            c.save()
        return redirect('cart:cartview')

class CartView(View):
    def get(self,request):
        u=request.user
        c = Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.subtotal()
        context={'cart':c,'total':total}
        return render(request,'cart.html',context)

class CartDecrement(View):
    def get(self,request,i):
        try:
            c = Cart.objects.get(id=i)
            if c.quantity > 1:
                c.quantity-=1
                c.save()
            else:
                c.delete()
        except:
            pass
        return redirect('cart:cartview')

class CartRemove(View):
    def get(self, request, i):
        try:
            c = Cart.objects.get(id=i)
            c.delete()
        except:
            pass
        return redirect('cart:cartview')

import razorpay
from cart.forms import OrderForm
from cart.models import OrderItems

class Checkout(View):
    def get(self,request):
        form_instance=OrderForm()
        context = {'form': form_instance}
        return render(request, 'checkout.html',context)
    def post(self,request):
        print(request.POST)
        form_instance = OrderForm(request.POST)
        if (form_instance.is_valid()):
            o=form_instance.save(commit=False)
            u=request.user
            o.user=u
            c = Cart.objects.filter(user=u)
            total = 0
            for i in c:
                total += i.subtotal()
            print(total)
            o.amount=int(total)
            o.save()
            if(o.payment_method=="ONLINE"):
                client=razorpay.Client(auth=('rzp_test_S60Hda5e7FXT1U','Zchz6Crdsy66M54LkqAeMGdO'))
                print(client)
                response_payment=client.order.create(dict(amount=o.amount*100,currency="INR"))
                print(response_payment)
                id=response_payment['id']
                o.order_id=id
                o.save()
                context={'payment':response_payment}
                return render(request, 'payment.html', context)
            else:
                id=uuid.uuid4().hex[:14]
                o.order_id='order_COD'+id
                o.is_ordered=True
                o.save()
                for i in c:
                    item=OrderItems.objects.create(order=o,product=i.product,quantity=i.quantity)
                    item.save()
                    item.product.stock -= item.quantity
                    item.product.save()

                c.delete()
                return render(request, 'payment.html')

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from cart.models import Order
@method_decorator(csrf_exempt,name="dispatch")
class Paymentsuccess(View):
    def post(self,request,i):
        u= User.objects.get(username=i)
        login(request,u)
        print(request.POST)
        id=request.POST['razorpay_order_id']
        o= Order.objects.get(order_id=id)
        o.is_ordered = True
        o.save()
        c=Cart.objects.filter(user=request.user)
        for i in c:
            item = OrderItems.objects.create(order=o, product=i.product, quantity=i.quantity)
            item.save()
            item.product.stock-=item.quantity
            item.product.save()
        c.delete()
        return render(request, 'paymentsuccess.html')

class OrderSummary(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context={'orders':o}
        return render(request, 'ordersummary.html',context)




