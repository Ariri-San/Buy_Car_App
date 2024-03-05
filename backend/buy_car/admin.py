from django.contrib import admin
from .models import BuyCar, UserSite

# Register your models here.

admin.site.register(UserSite)
admin.site.register(BuyCar)