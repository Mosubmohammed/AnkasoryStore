from django.shortcuts import render,get_object_or_404
from .cart import Cart
from Store.models import Product
from django.http import JsonResponse
# Create your views here.


def cart_summary(request):
    return render(request,"cart_summary.html",{})

def cart_add(request):
    cart=Cart(request)
    if request.POST.get('action') == 'post':
        product_id=int(request.POST.get('product_id'))
        product=get_object_or_404(Product,id=product_id)
        cart.add(product=product)
        
        return JsonResponse({'product Name':product.name})
    
        


def cart_delete(request):
        return render(request,"cart_delete.html",{})


def cart_update(request):
        return render(request,"cart_update.html",{})
