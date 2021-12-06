from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
    max_length=100,
    required = True,
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    username = forms.CharField(
    max_length=100,
    required = True,
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password1 = forms.CharField(
    required = True,
    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
    required = True,
    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    )
    cc_fullname = forms.CharField(
        required = False,
        label = 'Full Name on Credit Card',
        widget=forms.TextInput(attrs={'placeholder': 'Full name on credit card'}),
    )
    cc_number = forms.CharField(
        required = False,
        label = 'Fake Credit Card Number',
    )
    cc_exp = forms.CharField(
        required = False,
    )
    zip_code = forms.CharField(
        required = True,
    )
    phone = forms.CharField(
        required = True,
    )
    profile_pic = forms.ImageField(
        required = False, 
    )
    terms_and_cond = forms.BooleanField(
        required = True,
        label = 'I agree to the terms and conditions ',
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'cc_fullname', 'cc_number', 'cc_exp', 'zip_code', 
            'phone', 'profile_pic', 'terms_and_cond']


class UserUpdateForm(UserCreationForm):
    email = forms.EmailField(
    max_length=100,
    required = True,
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    username = forms.CharField(
    max_length=100,
    required = True,
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    cc_fullname = forms.CharField(
        required = False,
        label = 'Full Name on Credit Card',
        widget=forms.TextInput(attrs={'placeholder': 'Full name on credit card'}),
    )
    cc_number = forms.CharField(
        required = False,
    )
    cc_exp = forms.CharField(
        required = False,
    )
    zip_code = forms.CharField(
        required = True,
    )
    phone = forms.CharField(
        required = True,
    )
    profile_pic = forms.ImageField(
        required = False, 
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'cc_fullname', 'cc_number', 'cc_exp', 'zip_code', 
            'phone', 'profile_pic',]

            
    # class RegisterForm(UserCreationForm):
    # email = forms.EmailField(
    # max_length=100,
    # required = True,
    # help_text='Enter Email Address',
    # widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    # )
    # username = forms.CharField(
    # max_length=100,
    # required = True,
    # help_text='Enter Username',
    # widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    # )
    # password1 = forms.CharField(
    # help_text='Enter Password',
    # required = True,
    # widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    # )
    # password2 = forms.CharField(
    # required = True,
    # help_text='Enter Password Again',
    # widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    # )
    # class Meta:
    #     model = User
    #     fields = ['username', 'email', 'password1', 'password2',]