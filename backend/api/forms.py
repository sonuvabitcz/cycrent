from multiprocessing import AuthenticationError
from pyexpat import model
from urllib import request
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import date
from django.utils.translation import gettext_lazy as _

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


    def clean(self):
        cleaned_data = super().clean()
        raise ValidationError('Incorrect time')

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


def is_correct_time(date1, date2):
    c = date2 - date1
    if c.total_seconds() <= 0:
        print("Error: Incorrect time")
        return False
        # raise ValidationError("Incorrect time")
    return True


def is_time_free(date1, date2, bicycle):
    rents = RentingInfo.objects.filter(bicycle=bicycle)
    print(rents)
    for r in rents.all():
        # print(date1)
        # print(r.time_get)
        # print(date2)
        # print(r.time_return)
        # print("---------------------------")
        if date1 < r.time_get and date2 > r.time_get:
            print("Error: This time is already taken")
            return False
        elif date1 > r.time_get and date1 < r.time_return:
            print("Error: This time is already taken")
            return False
    return True


def is_enough_money(date1, date2, bicycle, user):
    print("===========================")
    print(user.profile.money)
    print(bicycle.price * (date2 - date1).total_seconds() / 60 / 60)
    print("===========================")
    if user.profile.money < bicycle.price * (date2 - date1).total_seconds() / 60 / 60:
        print("Error: Not enough money to rent the bicycle")
        return False
    return True


class RentBicycleForm(forms.ModelForm):
    time_get = forms.DateTimeInput()
    time_return = forms.DateTimeInput()
    bicycle = None
    user = None


    def __init__(self, *args, **kwargs):
        # self.obj_bicycle = kwargs.pop('bicycle', None)
        # self.obj_user = kwargs.pop('user', None)
        # print(self.obj_bicycle)
        # print(self.obj_user)
        super(RentBicycleForm, self).__init__(*args, **kwargs)


    class Meta:
        model = RentingInfo
        exclude = ('status',) # we'll set these fields later
        fields = ('time_get', 'time_return', 'bicycle', 'user',)
        widgets = {
        'time_get': forms.DateTimeInput(
            format=('%Y-%m-%d %H'),
            attrs={
                'onchange': 'showEndDate()',
                'id': 'time_get',
                'class': 'form-control',
                'placeholder': 'Select a time get',
                'type': 'datetime-local',
                'value': '2022-05-28T09:00',
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
                'value': '2022-05-30T22:00',
                'min': str(date.today()) + 'T22:00',
                'max': '2022-08-01T00:00'
                }),
        }


    def clean(self):
        # print(self.bicycle)
        # print(self.user)
        cleaned_data = super().clean()
        date1 = cleaned_data.get('time_get')
        date2 = cleaned_data.get('time_return')
        bicycle = cleaned_data.get('bicycle')
        user = cleaned_data.get('user')
        # print(bicycle)
        # print(user)
        if date1 and date2:
            if not is_correct_time(date1, date2):
                print("\n--------------\nError: Incorrect time IN\n--------------\n")
                self.add_error(None,'Incorrect time')
                self.add_error('time_get','Incorrect time')
                raise forms.ValidationError(_('Incorrect time'))
        if date1 and date2 and bicycle and user:
            if not is_time_free(date1, date2, bicycle):
                self.add_error(None,'This time is already taken')
                self.add_error('time_get','This time is already taken')
                raise forms.ValidationError(_('This time is already taken'))
            if not is_enough_money(date1, date2, bicycle, user):
                self.add_error(None,'Not enough money to rent the bicycle')
                self.add_error('time_get','Not enough money to rent the bicycle')
                raise forms.ValidationError(_('Not enough money to rent the bicycle'))
        print(self.errors)
        return self.cleaned_data


    # def init_model_fields(self, _dict: dict):
    #     self.bicycle = _dict['bicycle']
    #     self.user = _dict['user']

    # def clean(self, _dict: dict):
    #     print("--------------")
    #     print(_dict)
    #     print("--------------")
    #     cleaned_data = super().clean(_dict)
    #     date1 = cleaned_data.get('time_get')
    #     date2 = cleaned_data.get('time_return')
    #     if date1 and date2:
    #         if not is_correct_time(date1, date2):
    #             raise forms.ValidationError('Incorrect time')
    #         if not is_time_free(date1, date2):
    #             raise forms.ValidationError('Incorrect time')


class CancelRenting(forms.ModelForm):
    # cancel_renting = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = RentingInfo
        exclude = ('time_get', 'time_return', 'bicycle', 'user','status',)
        fields = ()


class EditRentingForm(forms.ModelForm):
    # edit_renting = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    time_get = forms.DateTimeInput()
    time_return = forms.DateTimeInput()

    def __init__(self, *args, **kwargs):
        super(EditRentingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = RentingInfo
        exclude = ('bicycle', 'user','status',)
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
                'value': '2022-05-31T09:00',
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
                'value': '2022-06-02T22:00',
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
