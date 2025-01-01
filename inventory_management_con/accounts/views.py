from django.shortcuts import render,redirect
from accounts.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .decorators import user_not_authenticated
from accounts_plans.models import Subscription
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import activation_token
from django.db.models.query_utils import Q
# Create your views here.

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('homepage')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("accounts/template_activate_account.html",{
        'user':user.username,
        'domain':get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token': activation_token.make_token(user),
        'protocol':'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user.username}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                         received activation link to confirm and complete the registration.<b>Note: </b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

@user_not_authenticated
def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            #messages.success(request, f"New account has been created: {user.username}")
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {
        'form' : form 
        })

@user_not_authenticated
def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserLoginForm(request=request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user.is_active == False:
                messages.error(request, f"Hello <b>{user.username}</b>, Maybe you didn't activate your account using your email address.")
                return redirect('login')

            if user is not None:
                if user.is_active:
                    login(request, user)
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
    
    subscription = Subscription.objects.filter(sub_user = request.user).first()

    context={
        'user':user,
        'form':form,
        'subscription':subscription
    }

    return render(request, 'accounts/profile.html',context)

    #return redirect('index')

def logout(request):
    auth_logout(request)
    return render(request, 'accounts/logout.html')

@login_required(login_url='login')
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    context = {
        'form':form
    }
    return render(request, 'accounts/password_reset_confirm.html',context)

@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("accounts/template_reset_password.html",{
                    'user':associated_user,
                    'domain':get_current_site(request).domain,
                    'uid':urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token':activation_token.make_token(associated_user),
                    'protocol':'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                                     """
                                    <h2>Password reset sent</h2><hr>
                                    <p>
                                        We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                                        You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                                        you registered with, and check your spam folder.
                                    </p>
                                    """
                                     )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")
            else:
                messages.success(request,
                                """
                                 <h2>Password reset sent</h2><hr>
                                    <p>
                                        We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                                        You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                                        you registered with, and check your spam folder.
                                    </p>
                                 """)
            return redirect('index')
        
        for key,error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    context = {
        'form':form
    }

    return render(request, 'accounts/password_reset.html', context)

def passwordResetConfirm(request,uidb64,token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and login now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        context = {
            'form':form
        }
        return render(request, 'accounts/password_reset_confirm.html',context)  
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect('index')