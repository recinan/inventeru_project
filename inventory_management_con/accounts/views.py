from django.shortcuts import render,redirect
from accounts.forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .decorators import user_not_authenticated
# Create your views here.

@user_not_authenticated
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

@user_not_authenticated
def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserLoginForm(request=request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    messages.success(request, f"Hello <b>{user.username}</b> You have been logged in")
                    return redirect('index')
            else:
                for key, error in list(form.errors.items()):
                    if key == 'captcha' and error[0] == 'This field is required.':
                        messages.error(request, "You must pass the reCAPTCHA test")
                        continue
                    
                    messages.error(request, error)
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {
        'form':form
    })

def profile_update(request,username):
    if request.method == "POST":
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            messages.success(request, f"{user_form.username}, Your profile has been updated!")
            return redirect('profile-update', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)

        return render(request, 'accounts/profile.html',{'form':form})

    return redirect('index')

def logout(request):
    auth_logout(request)
    return render(request, 'accounts/logout.html')

