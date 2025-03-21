from django.contrib import admin
from users.models import EtmsUser, VerificationToken

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    """Admin table for Users model"""
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'designation', 'is_active'
    ]


class VerificationTokenAdmin(admin.ModelAdmin):
    """Admin table for VerificationToken model"""
    list_display = ['user', 'token']

admin.site.register(EtmsUser, UserAdmin)
admin.site.register(VerificationToken, VerificationTokenAdmin)