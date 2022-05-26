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
    path('', HomePage.as_view(), name='home'),
    path('bicycles/', AllBicycles.as_view(), name='bicycles'),
    path('bicycle/<slug:bic_slug>', ShowBicycle.as_view(), name='bicycle'),
    path('sign_in/', show_sign_in, name='sign_in'),
    path('registrate/', RegistrateUser.as_view(), name='registrate'),
    path('my_bicycles/', MyBicycles.as_view(), name='my_bicycles'),
]
