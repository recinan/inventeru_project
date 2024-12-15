from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

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

    
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

