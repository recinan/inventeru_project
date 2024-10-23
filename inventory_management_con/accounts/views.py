from django.shortcuts import render,redirect
from accounts.forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {
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
    
    return render(request, 'login.html', {
        'form':form
    })

def logout(request):
    auth_logout(request)
    return render(request, 'logout.html')

