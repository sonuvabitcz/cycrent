from logging import raiseExceptions
from multiprocessing import AuthenticationError
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, Http404, HttpResponseForbidden
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.core.paginator import Paginator
from datetime import datetime
from django import forms

import re

from .serializers import RecipeSerializer #import the serializer we just created
from .models import *
from .forms import *
from .utils import *


class HomePage(DataMixin, TemplateView):
    template_name = 'api/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Main page', header_title='CycRent Home Page', header_descr='Almost as CycGo but only for renting')
        return dict(list(context.items()) + list(context_def.items()))


class AllBicycles(DataMixin, ListView):
    paginate_by = 1
    model = Bicycle
    template_name = 'api/bicycles.html'
    context_object_name = 'bicycles'
    
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

    # def get_form(self, form_class):
    #     request = self.request
    #     return form_class(request, **self.get_form_kwargs())


    # def get_form_kwargs(self):
    #     kwargs = super(ShowBicycle, self).get_form_kwargs()
    #     kwargs['bicycle'] = self.object
    #     kwargs['user'] = self.request.user
    #     return kwargs


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
        # try:
        #     self.is_time_free(date1, date2, self.object)
        #     self.is_enough_money(date1, date2, self.object, self.request.user)
        # except ValueError as e:
        #     form.add_error(None, e.message) # add none_field_error
        #     form.add_error('bicycle', e.message) # add none_field_error
        #     return self.form_invalid(form) 
        date1 = form.cleaned_data['time_get']
        date2 = form.cleaned_data['time_return']
        total_price = self.object.price * (date2 - date1).total_seconds() / 60 / 60
        form.instance.total_price = total_price
        form.instance.bicycle = self.object

        # update user's money after renting
        # self.request.user.profile.money-=total_price
        
        self.request.user.save()
        form.instance.user = self.request.user
        form.instance.status = True
        form.save()
        return super(ShowBicycle, self).form_valid(form)


    def get_success_url(self):
        return reverse_lazy('my_bicycles')


    # def form_invalid(self, form):
    #     return self.render_to_response(self.get_context_data(form=form))


    # def is_time_free(self, date1, date2, bicycle):
    #     pass
        # for r in bicycle.renting_users.all():
        #     if date1 < r.time_get and date2 > r.time_get or date1 > r.time_get and date1 < r.time_return:
        #         ex = ValueError()
        #         ex.message = "This time is already taken"
        #         raise ex


    # def is_enough_money(self, date1, date2, bicycle, user):
    #     if user.profile.money < bicycle.price * (date2 - date1).total_seconds() / 60 / 60:
    #         ex = ValueError()
    #         ex.message = "Not enough money to rent the bicycle"
    #         raise ex




class SignIn(DataMixin, LoginView):
    form_class = SignInUserForm
    template_name = 'api/sign_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Sign in')
        return dict(list(context.items()) + list(context_def.items()))

    def get_success_url(self):
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
        user = form.save()
        login(self.request, user)
        return redirect('home')


class MyOneBicycle(LoginRequiredMixin, DataMixin, UpdateView):
    model = RentingInfo
    template_name = 'api/my_bicycle_update_form.html'
    form_class = CancelRenting
    second_form_class = EditRentingForm
    login_url = reverse_lazy('sign_in')
    success_url = reverse_lazy('my_bicycles')
    slug_field = 'bic_slug'
    context_object_name = 'renting'
    

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyOneBicycle, self).get_context_data(**kwargs)
        context_def = self.get_user_context(title='My Bicycles', header_title='My Bicycles', header_descr='All my renting bicycles')
        if 'cancel_renting_form' not in context:
            context['cancel_renting_form'] = CancelRenting()
        if 'edit_renting_form' not in context:
            context['edit_renting_form'] = EditRentingForm()
            # context['edit_renting_form'] = EditRentingForm(initial={'time_get':context['model'].time_get}) # чтобы данные не стирались после неправильного ввода формы
        return dict(list(context.items()) + list(context_def.items()))


    # def get_object(self):
    #     return get_object_or_404(RentingInfo, pk=15)


    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name, self.get_context_data())

    
    def form_invalid(self, **kwargs):
        # return self.render_to_response(self.get_context_data(form=form))
        return self.render_to_response(self.get_context_data(**kwargs)) # very important because we have 2 forms


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {}
        # if r"^cancel_renting-" in request.POST:
        print("---- Inside post ")
        if 'cancel_renting' in request.POST:
            print("---- Inside if 'cancel_renting' ----")
            form_class = self.get_form_class()
            form_name = 'cancel_renting_form'
            # cancel_renting_form = CancelRenting(request.POST)

            # if cancel_renting_form.is_valid():
            #         # Here, save the response
            #         pass
            # else:
            #     context['cancel_renting_form'] = cancel_renting_form

        elif 'edit_renting' in request.POST:
            print("---- Inside if 'edit_renting' ----")
            form_class = self.second_form_class
            form_name = 'edit_renting_form'

            # edit_renting_form = EditRentingForm(request.POST)

            # if edit_renting_form.is_valid():
            #         # Here, save the comment
            #         pass
            # else:
            #     context['edit_renting_form'] = edit_renting_form
        

        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})

        # return render(request, self.template_name, self.get_context_data(**context))


    def form_valid(self, form):
        date1 = form.cleaned_data['time_get']
        date2 = form.cleaned_data['time_return']
        print("---- Inside form_valid ----")
        print(f"date1:{date1}, date2: {date2}")
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
        return RentingInfo.objects.filter(user=self.request.user)


def logout_user(request):
    logout(request)
    return redirect('sign_in')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Ohh... This page doesn\'t exists.\nCycRent</h1>')


# --- Methods ---


# def index(request):
#     user_list = User.objects.order_by('id')
#     template = loader.get_template('index.html')
#     context = {
#         'user_list': user_list,
#     }

#     return HttpResponse(template.render(context, request))


# def index(request):
#     if(request.GET):
#         print(request.GET)
#     users = User.objects.all()
#     cards = BankCard.objects.all()
#     context = {
#         'users':users,
#         'menu':menu,
#         'cards':cards,
#         'title':'Main page',
#         'card_selected':0,
#         'header_title': 'CycRent Home Page',
#         'header_descr': 'Almost as CycGo but only for renting',
#         'is_signed_in': is_signed_in,
#     }
#     return render(request, 'api/index.html', context=context)


# def show_all_bicycles(request):
#     bicycles = Bicycle.objects.all()
#     context = {
#         'bicycles':bicycles,
#         'menu':menu,
#         'title':'Bicycles',
#         'header_title': "All bicycles for you",
#         'header_descr': "Big wheels, big travel, big fun",
#     }
#     return render(request, 'api/bicycles.html', context=context)


# def show_bicycle(request, bic_slug : str):
#     bicycle = get_object_or_404(Bicycle, slug=bic_slug)
#     context = {
#         'bicycle': bicycle,
#         'menu': menu,
#         'title': bicycle.brand + " " + bicycle.model,
#         'header_title': bicycle.brand + " " + bicycle.model,
#         'header_descr': "Big wheels, big travel, big fun",
#     }
#     return render(request, 'api/bicycle.html', context=context)


# def show_sign_in(request):
#     context = {
#         'menu':menu,
#         'title':'Sign In',
#     }
#     return render(request, 'api/sign_in.html', context=context)


# def show_registrate(request):
#     if request.method == 'POST':
#         form = RegistrateUserForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = RegistrateUserForm()
#     context = {
#         'menu':menu,
#         'title': "Registrate",
#         'title':'Sign In',
#         'form':form
#     }
#     return render(request, 'api/registrate.html', context=context)