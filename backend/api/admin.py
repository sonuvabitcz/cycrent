from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *


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
    list_display = ('brand', 'model', 'slug', 'type', 'wheel_size', 'fork', 'price', 'get_rentings')
    prepopulated_fields = {"slug":("brand","model")}

    def get_rentings(self, obj):
        return "\n".join([p.username for p in obj.renting_users.all()])

class RentingInfoAdmin(admin.ModelAdmin):
    list_display = ('bicycle', 'user', 'time_get', 'time_return', 'status')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'money', 'date_register')

# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(BankCard, BankCardAdmin)
# admin.site.register(User, UserAdmin)
admin.site.register(Bicycle, BicycleAdmin)
admin.site.register(RentingInfo, RentingInfoAdmin)
admin.site.register(Profile, ProfileAdmin)
