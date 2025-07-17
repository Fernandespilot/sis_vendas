from django.contrib import admin
from .models import Promotor
from django.contrib.auth.models import User
from django.contrib import admin

@admin.register(Promotor)
class PromotorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email')

