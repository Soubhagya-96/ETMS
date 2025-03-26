from django.contrib import admin
from users.models import EtmsUser, VerificationToken, UserToken

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    """Admin table for Users model"""
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'designation', 'is_active'
    ]


class VerificationTokenAdmin(admin.ModelAdmin):
    """Admin table for VerificationToken model"""
    list_display = ['user', 'token']


class UserTokenAdmin(admin.ModelAdmin):
    """Admin table for UserToken model"""
    list_display = ['user', 'access_token', 'refresh_token', 'created_at']

admin.site.register(EtmsUser, UserAdmin)
admin.site.register(VerificationToken, VerificationTokenAdmin)
admin.site.register(UserToken, UserTokenAdmin)