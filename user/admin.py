from django.contrib import admin

from .models import User, ActivationCode


class UserAdmin(admin.ModelAdmin):
    list_display = ("username","is_active")
    
class ActivationCodeManager(admin.ModelAdmin):
    list_display = ("user", "code")

admin.site.register(User,UserAdmin)
admin.site.register(ActivationCode, ActivationCodeManager)
