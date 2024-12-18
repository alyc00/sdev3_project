from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile 

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'email', 
        'username',
        'first_name',
        'last_name',
        'is_staff',
    ]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
