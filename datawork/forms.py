from django import forms
from datawork.models import *


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ("user", )
