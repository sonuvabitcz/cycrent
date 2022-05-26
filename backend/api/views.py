from multiprocessing import AuthenticationError
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, Http404
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator

from .serializers import RecipeSerializer #import the serializer we just created
from .models import Bicycle, RentingInfo
from .forms import *
from .utils import *


# def index(request):
#     user_list = User.objects.order_by('id')
#     template = loader.get_template('index.html')
#     context = {
#         'user_list': user_list,
#     }

#     return HttpResponse(template.render(context, request))


class HomePage(DataMixin, TemplateView):
    template_name = 'api/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Main page', header_title='CycRent Home Page', header_descr='Almost as CycGo but only for renting')
        return dict(list(context.items()) + list(context_def.items()))


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


class ShowBicycle(DataMixin, DetailView):
    model = Bicycle
    template_name = 'api/bicycle.html'
    slug_url_kwarg = 'bic_slug'
    context_object_name = 'bicycle'
    # success_url = reverse_lazy('home') # если нет get_upsolute_url то так прописываем маршрут какая странгица должна открыться

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title=context['bicycle'].brand + " " + context['bicycle'].model, header_title=context['bicycle'].brand + " " + context['bicycle'].model, header_descr='Big wheels, big travel, big fun')
        return dict(list(context.items()) + list(context_def.items()))


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

class SignIn(DataMixin, LoginView):
    form_class = SignInUserForm
    template_name = 'api/sign_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Sign in')
        return dict(list(context.items()) + list(context_def.items()))

    def get_success_url(self):
        return reverse_lazy('my_bicycles')


def show_sign_in(request):
    context = {
        'menu':menu,
        'title':'Sign In',
    }
    return render(request, 'api/sign_in.html', context=context)


class RegistrateUser(DataMixin, CreateView):
    form_class = RegistrateUserForm
    template_name = 'api/registrate.html'
    success_url = reverse_lazy('home')
    success_message = "Your profile was created successfully"
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_def = self.get_user_context(title='Registrate')
        return dict(list(context.items()) + list(context_def.items()))


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

# def show_db(request):
#     user_list = User.objects.order_by('id')
#     template = loader.get_template('index.html')
#     context = {
#         'user_list': user_list,
#     }
#     return HttpResponse(template.render(context, request))

# def index_args(request, sms : str):
#     if(request.GET):
#         print(request.GET)
#     if(len(sms) > 10):
#         # raise Http404()
#         return redirect('home') # url поменялся временно 302
#         return redirect('/', permanent=True) # url поменялся навсегда 301
#     return HttpResponse(f"Hello world {sms}")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Ohh... This page doesn\'t exists.\nCycRent</h1>')

# так тоже можно
# context = {'user_list': user_list}
# return render(request, 'index.html', context)

# class recipe_view_set(viewsets.ModelViewSet):
#     # define queryset
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer