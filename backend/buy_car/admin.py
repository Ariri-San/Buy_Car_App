from django.contrib import admin
from .models import BuyCar, Car, Captcha, HistoryBuyCar

# Register your models here.

admin.site.register(Car)
admin.site.register(BuyCar)
admin.site.register(HistoryBuyCar)
admin.site.register(Captcha)