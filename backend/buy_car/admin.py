from django.contrib import admin
from .models import BuyCar, Car, Captcha

# Register your models here.

admin.site.register(Car)
admin.site.register(BuyCar)
admin.site.register(Captcha)