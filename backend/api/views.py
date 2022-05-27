from logging import raiseExceptions
from multiprocessing import AuthenticationError
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, Http404, HttpResponseForbidden
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.core.paginator import Paginator
from datetime import datetime

from .serializers import RecipeSerializer #import the serializer we just created
from .models import Bicycle, RentingInfo
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
    # success_message = "You successfully rent the bicycle"
    # bicycle_context = context_object_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(
            title=context['bicycle'].brand + " " + context['bicycle'].model, 
            header_title=context['bicycle'].brand + " " + context['bicycle'].model, 
            header_descr='Big wheels, big travel, big fun'
        )
        # context['form'] = RentBicycleForm()
        context['form'] = self.get_form()
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
        # validate correct data
        date1 = form.instance.time_get
        date2 = form.instance.time_return
        c = date2 - date1
        if c.total_seconds() < 0:
            # print("Error bla bla bla")
            # raise ValidationError("bla bla bla")
            return HttpResponseForbidden()
        form.instance.total_price = self.object.price * c.total_seconds() / 60 / 60
        
        # validate if this date is taken
        for r in self.object.renting_users:
            if date1 < r.time_get and date2 > r.time_get:
                return HttpResponseForbidden()
            elif date1 > r.time_get and date1 < r.time_return:
                print("Error This time already is taken")
                raise ValidationError("This time already is taken")
                # return HttpResponseForbidden()
        form.instance.bicycle = self.object
        form.instance.user = self.request.user
        form.instance.status = True
        form.save()
        return super(ShowBicycle, self).form_valid(form)
        # return redirect('my_bicycle')
    
    def get_success_url(self):
        return reverse_lazy('my_bicycles')



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


class MyBicycles(LoginRequiredMixin, DataMixin, ListView):
    # model = Bicycle.objects.filter    (renting_users__user__login='current login')
    model = Bicycle
    template_name = 'api/my_bicycles.html'
    context_object_name = 'bicycles'
    login_url = reverse_lazy('sign_in') # куда перенаправляется если не зареган и пытается открыть страницу
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='My Bicycles', header_title='My Bicycles', header_descr='All my renting bicycles')
        return dict(list(context.items()) + list(context_def.items()))


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