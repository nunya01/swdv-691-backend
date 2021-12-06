from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Profile, Tool
from django import forms
from django.contrib.auth.models import User


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('cc_number', 'cc_exp', 'cc_fullname','zip_code', 'phone', 'profile_pic', 'terms_and_cond',)
        labels = {
            'cc_number': _('* Credit Card #:'),
            'cc_exp': _('* Credit Card Exp:'),
            'cc_fullname': _('* Full name on Credit Card:'),
            'zip_code': _('Zip Code:'),
            'profile_pic': _('Profile Image:'),
            'terms_and_cond': _('I agree to the terms and conditions:'),
        }
    def clean(self):
        super(ProfileForm, self).clean()
        tac = self.cleaned_data.get('terms_and_cond')
        if tac != True:
            self._errors['terms_and_cond'] = self.error_class(['You must agree to the terms and conditions to use this site!'])
        return self.cleaned_data


class ToolForm(ModelForm):
    class Meta:
        model = Tool
        fields = ('name', 'description', 'tool_value', 'for_sale', 'visible', 'tool_pic')
        labels = {
            'tool_value': _('Tool Value ($ USD)')
        }


class UserUpdateForm(ModelForm):
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
    class Meta:
        model = User
        fields = ['username', 'email',]


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('cc_number', 'cc_exp', 'cc_fullname','zip_code', 'phone', 'profile_pic',)
        labels = {
            'cc_number': _('* Credit Card #:'),
            'cc_exp': _('* Credit Card Exp:'),
            'cc_fullname': _('* Full name on Credit Card:'),
            'zip_code': _('Zip Code:'),
            'profile_pic': _('Profile Image:'),
        }