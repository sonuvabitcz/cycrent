from logging import raiseExceptions
from multiprocessing import AuthenticationError
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.core.paginator import Paginator
from datetime import datetime
from django import forms
import asyncio
from asgiref.sync import sync_to_async
import logging

import re

from .models import *
from .forms import *
from .utils import *

logger = logging.getLogger(__name__)

class HomePage(DataMixin, TemplateView):
    template_name = 'api/index.html'
    logger.warning('Current template_name: index.html')
    logger.info('Default home page')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Main page', header_title='CycRent Home Page', header_descr='Almost CycGo but only about renting')
        return dict(list(context.items()) + list(context_def.items()))


class AllBicycles(DataMixin, ListView):
    paginate_by = 3
    model = Bicycle
    template_name = 'api/bicycles.html'
    context_object_name = 'bicycles'
    logger.warning('Current template_name: bicycles.html')
    logger.info('Show all bicycles')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Bicycles', header_title='All bicycles for you', header_descr='Big wheels, big travel, big fun')
        return dict(list(context.items()) + list(context_def.items()))
    # def get_queryset(self): # задаем определенные параметры для отображения списка
        # return Bicycle.objects.filter(price__gte=50)

    # def get_queryset(self):
    #     return Bicycle.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


class ShowBicycle(FormMixin, DataMixin, DetailView):
    model = Bicycle
    form_class = RentBicycleForm
    template_name = 'api/bicycle.html'
    slug_url_kwarg = 'bic_slug'
    context_object_name = 'bicycle'
    success_url = reverse_lazy('my_bicycles')
    logger.warning('Current template_name: bicycle.html')
    logger.info('Show one particular bicycle')
    # raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(
            title=context['bicycle'].brand + " " + context['bicycle'].model, 
            header_title=context['bicycle'].brand + " " + context['bicycle'].model, 
            header_descr='Big wheels, big travel, big fun'
        )
        context['form'] = RentBicycleForm(initial={'bicycle':self.object, 'user':self.request.user})
        # b = RentingInfo(bicycle=self.object, user=self.request.user)
        # context['form'] = RentBicycleForm(bicycle=self.object, user=self.request.user)
        # context['form'] = self.get_form()
        return dict(list(context.items()) + list(context_def.items()))

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        # asyncio.run(self.async_save_data(form))
        logger.info(f'Created renting {self.request.user} {2} {form.instance.bicycle}')
        date1 = form.cleaned_data['time_get']
        date2 = form.cleaned_data['time_return']
        total_price = self.object.price * (date2 - date1).total_seconds() / 60 / 60
        self.request.user.profile.money-=total_price
        date1 = form.cleaned_data['time_get']
        date2 = form.cleaned_data['time_return']
        total_price = self.object.price * (date2 - date1).total_seconds() / 60 / 60

        form.instance.total_price = total_price
        form.instance.bicycle = self.object

        # update user's money after renting
        print('Money before write off')
        print(self.request.user.profile.money)
        self.request.user.profile.money-=total_price
        
        self.request.user.save()
        print('Money after write off')
        print(self.request.user.profile.money)
        form.instance.user = self.request.user
        form.instance.status = True
        form.save()
        return super(ShowBicycle, self).form_valid(form)


    async def async_save_data(self, form):
        date1 = form.cleaned_data['time_get']
        date2 = form.cleaned_data['time_return']
        total_price = self.object.price * (date2 - date1).total_seconds() / 60 / 60
        self.request.user.profile.money-=total_price
        task2 = asyncio.create_task(self.update_user_money(total_price))
        task1 = asyncio.create_task(self.create_bicycle(form, total_price))

        print("Before gather")
        await asyncio.gather(task2, task1)
        print("Have updated all objects")

    async def create_bicycle(self, form, total_price):
        print("Get create bicycle task to do")
        form.instance.total_price = total_price
        form.instance.bicycle = self.object
        form.instance.user = self.request.user
        form.instance.status = True
        # await asyncio.sleep(1)
        print("Get create bicycle task to do ... 2")
        await sync_to_async(form.save)()
        print("Have created bicycle")
    
    async def update_user_money(self, total_price):
        print("Get update user money task to do")
        # await asyncio.sleep(6)
        print("Get update user money task to do ... 2")
        await sync_to_async(self.request.user.save)()
        print("Have updated user money")


    def get_success_url(self):
        return reverse_lazy('my_bicycles')


    # test async
    # async def print_nums(self):
    #     num = 1
    #     while num < 100:
    #         print(num)
    #         num += 1
    #         await asyncio.sleep(0.1)

    # async def print_time(self):
    #     count = 0
    #     while count < 18:
    #         if count % 3 == 0:
    #             print(f"{count} seconds have passed")
    #         count += 1
    #         await asyncio.sleep(1)


    # async def event_manager(self):
    #     task1 = asyncio.create_task(self.print_nums())
    #     task2 = asyncio.create_task(self.print_time())

    #     await asyncio.gather(task1, task2)
    
    # asyncio.run(event_manager(self))

    # def form_invalid(self, form):
    #     return self.render_to_response(self.get_context_data(form=form))


class SignIn(DataMixin, LoginView):
    form_class = SignInUserForm
    template_name = 'api/sign_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Sign in')
        return dict(list(context.items()) + list(context_def.items()))

    def get_success_url(self):
        # logger.info(f'New logging in {0} ({1})', {self.request.user.username, self.request.user.password})
        return reverse_lazy('my_bicycles')


class RegistrateUser(DataMixin, CreateView):
    form_class = RegistrateUserForm
    template_name = 'api/registrate.html'
    success_url = reverse_lazy('home')
    success_message = "Your profile was created successfully"
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Registrate')
        return dict(list(context.items()) + list(context_def.items()))

    def form_valid(self, form):
        # logger.info(f'New user have been registrated in {1} ({2})', {form.user.username, form.user.password})
        # logger.info(f'{0}', self.success_message)
        user = form.save()
        login(self.request, user)
        return redirect('home')


class MyOneBicycle(LoginRequiredMixin, DataMixin, UpdateView):
    model = RentingInfo
    template_name = 'api/my_bicycle_update_form.html'
    form_class = EditRentingForm
    second_form_class = CancelRenting
    login_url = reverse_lazy('sign_in')
    success_url = reverse_lazy('my_bicycles')
    slug_field = 'bic_slug'
    context_object_name = 'renting'
    

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(
            title='My Bicycles', 
            header_title='My Bicycles',
            header_descr='All my renting bicycles'
        )
        if 'cancel_renting_form' not in context:
            context['cancel_renting_form'] = CancelRenting()
        if 'edit_renting_form' not in context:
            # context['edit_renting_form'] = EditRentingForm(user=self.request.user)
            print("in view user:" + str(self.request.user))
            context['edit_renting_form'] = EditRentingForm(initial={'user': self.request.user, 'bicycle': self.object.bicycle})
            # context['edit_renting_form'] = EditRentingForm(initial={'time_get':context['model'].time_get}) # чтобы данные не стирались после неправильного ввода формы
        return dict(list(context.items()) + list(context_def.items()))


    def is_enough_money(self, form, date1, date2):
        new_total_price = self.object.bicycle.price * (self.object.time_return - self.object.time_get).total_seconds() / 60 / 60
        old_total_price = self.object.bicycle.price * (date2 - date1).total_seconds() / 60 / 60
        print(old_total_price)
        print(new_total_price)
        money_after_editing = self.request.user.profile.money + old_total_price - new_total_price
        if money_after_editing < 0:
            logger.info('Error: Not enough money to rent the bicycle')
            return False
        return True


    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        if 'cancel_renting' in request.POST:
            print("---- Inside if 'cancel_renting' ----")
            form_class = self.second_form_class
            form_name = 'cancel_renting_form'
        elif 'edit_renting' in request.POST:
            print("---- Inside if 'edit_renting' ----")
            form_class = self.get_form_class()
            form_name = 'edit_renting_form'        

        old_time_get = self.object.time_get
        old_time_return = self.object.time_return
        form = self.get_form(form_class)
        if form.is_valid():
            if 'edit_renting' in request.POST:
                if not self.is_enough_money(form, old_time_get, old_time_return):
                    form.add_error(None,'Not enough money to rent the bicycle')
                    print("Error2: Not enough money to rent the bicycle")
                if form.is_valid():
                    return self.form_valid(form)
                return self.form_invalid(**{form_name: form})
        else:
            print("FORM INVALID")
            print(form.errors)
            return self.form_invalid(**{form_name: form})

        # return render(request, self.template_name, self.get_context_data(**context))

    
    def form_invalid(self, **kwargs):
        # return self.render_to_response(self.get_context_data(form=form))
        return self.render_to_response(self.get_context_data(**kwargs)) # very important because we have 2 forms


    def form_valid(self, form):
        print("FORM VALID")
        # print("form is: " + str(form))
        date1 = form.cleaned_data['time_get']
        date2 = form.cleaned_data['time_return']
        print("---- Inside form_valid ----")
        print(f"date1:{date1}, date2: {date2}")
        total_price = self.object.bicycle.price * (date2 - date1).total_seconds() / 60 / 60
        self.request.user.profile.money += self.object.total_price
        self.object.total_price = total_price
        self.request.user.profile.money -= self.object.total_price
        self.request.user.save()
        print(self.request.user.profile.money)
        print("SUCCESS")
        return super(MyOneBicycle, self).form_valid(form)


class MyBicycles(LoginRequiredMixin, DataMixin, ListView):
    model = RentingInfo
    template_name = 'api/my_bicycles.html'
    context_object_name = 'rents'
    login_url = reverse_lazy('sign_in')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='My Bicycles', header_title='My Bicycles', header_descr='All my renting bicycles')
        context['usr_money'] = self.request.user.profile.money
        context['usr_username'] = self.request.user.username
        context['usr_email'] = self.request.user.email
        rents = self.get_queryset()
        context['usr_count_bicycles'] = rents.count
        print(RentingInfo.objects.filter(user=self.request.user))
        return dict(list(context.items()) + list(context_def.items()))

    def get_queryset(self): # задаем определенные параметры для отображения списка
        return RentingInfo.objects.filter(user=self.request.user).order_by('time_get')


def logout_user(request):
    logout(request)
    return redirect('sign_in')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Ohh... This page doesn\'t exists.\nCycRent</h1>')