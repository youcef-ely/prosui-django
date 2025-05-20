from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'first_login')
    list_filter = ('role', 'first_login')
    search_fields = ('email', 'first_name', 'last_name')
