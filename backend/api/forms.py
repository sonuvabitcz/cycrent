from multiprocessing import AuthenticationError
from pyexpat import model
from urllib import request
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import date

from .models import *

class RegistrateUserForm(UserCreationForm):
    first_name = forms.CharField(label='First name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last name', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.fields['bank_card'].empty_label = "Choose..."

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # 'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+375'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            # 'profile_photo': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super(RegistrateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    # def clean_first_name(self):
    #     first_name = self.cleaned_data['first_name']
    #     if len(first_name) > 50:
    #         raise ValidationError('Too long name. Must be less then 50 symbols')
    #     return first_name


class SignInUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id':'floatingInput',
            'placeholder':'username'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id':'floatingInput',
            'placeholder':'password'
        })
    )


class RentBicycleForm(forms.ModelForm):
    time_get = forms.DateTimeInput()
    time_return = forms.DateTimeInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = RentingInfo
        exclude = ('bicycle', 'user', 'status',) # we'll set these fields later
        fields = ('time_get', 'time_return',)
        widgets = {
        'time_get': forms.DateTimeInput(
            format=('%Y-%m-%d %H'),
            attrs={
                'onchange': 'showEndDate()',
                'id': 'time_get',
                'class': 'form-control', 
                'placeholder': 'Select a time get',
                'type': 'datetime-local',
                'value': '2022-05-27T09:00',
                'min': str(date.today()) + 'T09:00',
                'max': '2022-08-01T00:00'
                }),
        'time_return': forms.DateTimeInput(
            format=('%Y-%m-%d %H'),
            attrs={
                'onchange': 'showEndDate()',
                'id': 'time_return',
                'class': 'form-control', 
                'placeholder': 'Select a time return',
                'type': 'datetime-local',
                'value': '2022-05-28T22:00',
                'min': str(date.today()) + 'T22:00',
                'max': '2022-08-01T00:00'
                }),
        }



# class RegistrateUser(forms.Form):
#     first_name = forms.CharField(max_length=50, label='First name', widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages={'required':'Valid first name is required'}, required=True)
#     last_name = forms.CharField(max_length=50, label='Last name', widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages={'required':'Valid last name is required'})
#     login = forms.CharField(max_length=100, label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages={'required':'Valid login is required'})
#     password = forms.CharField(max_length=100, label='Password', widget=forms.TextInput(attrs={'class': 'form-control'}), error_messages={'required':'Valid password is required'})
#     telephone = forms.CharField(max_length=15, required=False, label='Telephone', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+375'}), error_messages={'required':'Valid telephone is required'})
#     bank_card = forms.ModelChoiceField(queryset=BankCard.objects.all(), empty_label="Choose...", label='Bank card', error_messages={'required':'Please select your bank card'})
