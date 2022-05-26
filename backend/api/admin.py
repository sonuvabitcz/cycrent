from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Bicycle, RentingInfo


# class CustomUserAdmin(UserAdmin):
#     model = CustomUser

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'login', 'telephone', 'password', 'bank_card', 'profile_photo')
#     list_display_links = ('first_name', 'last_name', 'password')
#     search_fields = ('first_name',)
#     list_editable = ('login',)
#     list_filter = ('bank_card',)


# class BankCardAdmin(admin.ModelAdmin):
#     list_display = ('num', 'ccv', 'money')


class BicycleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'slug', 'type', 'wheel_size', 'fork', 'description', 'price', 'description', 'price')
    prepopulated_fields = {"slug":("brand","model")}


# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(User, UserAdmin)
# admin.site.register(BankCard, BankCardAdmin)
admin.site.register(Bicycle, BicycleAdmin)
