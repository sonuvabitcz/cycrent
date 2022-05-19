from rest_framework import viewsets
from django.http import HttpResponse
from django.template import loader
from .serializers import RecipeSerializer #impor the serializer we just created
from .models import Recipe, User


def index(request):
    user_list = User.objects.order_by('id')
    template = loader.get_template('index.html')
    context = {
        'user_list': user_list,
    }

    return HttpResponse(template.render(context, request))

# так тоже можно
# context = {'user_list': user_list}
# return render(request, 'index.html', context)

class recipe_view_set(viewsets.ModelViewSet):
    # define queryset
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer