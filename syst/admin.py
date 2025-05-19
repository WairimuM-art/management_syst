from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile

from django.contrib.auth.models import User

# Register your models here.
# admin.site.register(Login)
# admin.site.register(Register)
admin.site.register(UserProfile)

# mixing profile info and user info
class ProfilInLine(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfilInLine]

# unregister old way

admin.site.unregister(User)

# register new way

admin.site.register(User, UserAdmin)