from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Customer

class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'login-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'login-input'}))

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'login-input', 'placeholder': 'Your Password'})
        self.fields['password2'].widget.attrs.update({'class': 'login-input', 'placeholder': 'Repeat your Password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'login-input'}))
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'login-input'}))

    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'login-input', 'placeholder': 'Your Password'})
        self.fields['name'].widget.attrs.update({'class': 'login-input', 'placeholder': 'Enter your full name'})

    class Meta:
        model = Customer
        fields = ['username', 'password', 'email', 'name']

