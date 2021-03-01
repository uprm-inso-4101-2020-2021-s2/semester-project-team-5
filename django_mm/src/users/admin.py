from django.contrib import admin

# Register your models here.


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User

class UserAdmin(admin.ModelAdmin):
    model=User
    list_display = ['username']

    # def changelist_view(self, request, extra_context=None):


admin.site.register(User, UserAdmin)