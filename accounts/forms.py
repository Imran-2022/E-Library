from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm


class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter amount to deposit'})
    )

class RegistrationForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']


class ChangeUserForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']


