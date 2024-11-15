from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
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
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
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
        messages.error(request, 'That Category does not exist')
        
        return redirect('home')