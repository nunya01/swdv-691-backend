from django.forms import forms, ModelForm, BooleanField
from django.utils.translation import gettext_lazy as _
from .models import Profile, Tool

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('cc_number', 'cc_exp', 'cc_fullname','zip_code', 'phone', 'terms_and_cond')
        labels = {
            'cc_number': _('* Credit Card #:'),
            'cc_exp': _('* Credit Card Exp:'),
            'cc_fullname': _('* Full name on Credit Card:'),
            'zip_code': _('Zip Code:'),
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
        fields = ('name', 'description', 'tool_value', 'for_sale', 'visible', 'img_url')
