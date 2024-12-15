from django.shortcuts import render,redirect
from accounts.forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request, f"New account has been created: {user.username}")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {
        'form' : form 
        })

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('index')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {
        'form':form
    })

def logout(request):
    auth_logout(request)
    return render(request, 'accounts/logout.html')

