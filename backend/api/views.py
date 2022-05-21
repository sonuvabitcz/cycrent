from rest_framework import viewsets
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, Http404
from django.template import loader
from django.shortcuts import render, redirect
from .serializers import RecipeSerializer #import the serializer we just created
from .models import *


# def index(request):
#     user_list = User.objects.order_by('id')
#     template = loader.get_template('index.html')
#     context = {
#         'user_list': user_list,
#     }

#     return HttpResponse(template.render(context, request))

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

def index(request):
    if(request.GET):
        print(request.GET)
    bicycles = Bicycle.objects.all()
    context = {
        'bicycles':bicycles,
        'menu':menu,
        'title':'Main page'
    }
    return render(request, 'api/index.html', context)
    # return HttpResponse(f"Hello world")


def about(request):
    if(request.GET):
        print(request.GET)
    return render(request, 'api/about.html', {'menu':menu,'title':'About page'})
    # return HttpResponse(f"Hello world")

def addpage(request):
    return HttpResponse("Добавление статьи")

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

def show_post(request, post_id):
    return HttpResponse(f"Статья с id = {post_id}")

def show_db(request):
    user_list = User.objects.order_by('id')
    template = loader.get_template('index.html')
    context = {
        'user_list': user_list,
    }
    return HttpResponse(template.render(context, request))

def index_args(request, sms : str):
    if(request.GET):
        print(request.GET)
    if(len(sms) > 10):
        # raise Http404()
        return redirect('home') # url поменялся временно 302
        return redirect('/', permanent=True) # url поменялся навсегда 301
    return HttpResponse(f"Hello world {sms}")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Ohh... This page doesn\'t exists.\nCycRent</h1>')

# так тоже можно
# context = {'user_list': user_list}
# return render(request, 'index.html', context)

# class recipe_view_set(viewsets.ModelViewSet):
#     # define queryset
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer