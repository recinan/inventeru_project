from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class UserRegisterForm(UserCreationForm):

    email = forms.EmailField(help_text="A valid email address for verification, please.", required=True)
    username = forms.CharField(help_text="Choose a unique username, please.", required=True)
    phone_number = forms.CharField(help_text="Choose a unique phone number, please.", required=True)
    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','username','email','phone_number','password1','password2']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        
        return user

    
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Username or Email'}),
        label = "Username or Email")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder':'Password'}
    ))

    captcha = ReCaptchaField(widget = ReCaptchaV2Checkbox())

