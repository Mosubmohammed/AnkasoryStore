from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm
from Payment.forms import ShippingForm
from Payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from Cart.cart import Cart
# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})

def about(request):
    return render(request, 'about.html',{})


def login_user(request):
    
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request, user)
            
            #do sume sshopping sutuff
            current_user=Profile.objects.get(user__id=request.user.id)
            #get there saved cart from db
            saved_cart=current_user.old_cart
            #convert saved_cart string to dic
            if saved_cart:
                #convert to dic using JSON
                converted_cart=json.loads(saved_cart)
                #add loaded cart dic to our session
                cart=Cart(request)
                #loop thru the cart and add the item from the db
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)
                    
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.success(request, 'there was an error, trying to login')
            return redirect('login')
        
    else:        
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

def register_user(request):
    form=SignUpForm()
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}!-please fill out Your User Info Below....')
            return redirect('update_info')
        else:
            messages.error(request, 'Registration failed, please try again.')
            return redirect('register')
    else:
        
        return render(request,'register.html', {'form': form})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def category(request, foo):
    #!Replace Hyphens with spaces
    foo=foo.replace('-', ' ')
    #!grap the gategory from the url
    try:
        category=Category.objects.get(name=foo)
        products=Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, 'That Category does not exist')
        
        return redirect('home')
    
def category_summary(request):
    categories=Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form=UpdateUserForm(request.POST or None,instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request,current_user)
            messages.success(request, 'Your profile has been updated successfully!')
            
            return redirect('home')
            
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, 'You need to be logged in to update your profile')
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form=ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated successfully,please login again....')
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:    
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, 'You need to be logged in to update your password')
        return redirect('home')

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)

        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            shipping_user = ShippingAddress(user=request.user)  # Create a new instance if it doesn't exist

        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your Info Has Been Updated!!")
            return redirect('home')

        return render(request, "update_info.html", {'form': form, 'shipping_form': shipping_form})

    else:
        messages.error(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')


def search(request):
    if request.method == 'POST':
        searched=request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains = searched)| Q(description__icontains = searched))
        if not searched:
            messages.success(request, 'No results found for your search')
            return redirect('search')
        else:
            return render(request, 'search.html', {'searched': searched})

        
    else:
        return render(request, 'search.html', {})
    