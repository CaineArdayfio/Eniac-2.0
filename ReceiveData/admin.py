from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserResponse

class UserResponseDate(admin.ModelAdmin):
    readonly_fields = ('response_time',)

admin.site.register(UserResponse, UserResponseDate)
