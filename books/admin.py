from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Books)
admin.site.register(models.Order)
admin.site.register(models.Comment)