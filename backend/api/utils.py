menu = [{'title': "Home", 'url_name': 'home'},
        {'title': "Bicycles", 'url_name': 'bicycles'},
        {'title': "My bicycles", 'url_name': 'my_bicycles'},
]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cp_menu = menu.copy()
        # если юзер не вошел, из меню убирается My Bicycles
        if not self.request.user.is_authenticated:
            cp_menu.pop(2)
        context['menu'] = cp_menu
        context['user'] = self.request.user
        return context