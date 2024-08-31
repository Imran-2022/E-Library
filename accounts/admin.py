# accounts/admin.py

from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)
