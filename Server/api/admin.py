from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('User_credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','username')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name','username','password1','password2'),
        }),
    )
    list_display = ('id','email','name', 'is_admin',)
    list_filter = ('is_admin','is_active',)
    search_fields = ('email', 'name','username',)
    ordering = ('email',)
    filter_horizontal = ()

# Register your models here
admin.site.register(User, UserAdmin)
admin.site.register(Guest)
admin.site.register(CodeSnippet)
admin.site.register(OCRProcess)
