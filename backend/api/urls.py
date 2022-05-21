from django.urls import path, include
from .views import *
from rest_framework import routers

# обработка исключений при запросах к серверу
# handler500 - ошибка сервера
# handler403 - доступ запрещен
# handler400 - невозможно обработать запрос

# router = routers.DefaultRouter()
# router.register(r'api', index) #the route tha will be used to access your API on the browser
urlpatterns = [
    path('addpage/', addpage, name='add_page'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('post/<int:post_id>', show_post, name='post'),
    path('<slug:sms>/', index_args),
    # path('<slug:sms>/', index), # лучше слаги использовать
]
