from django.db import models
from django.conf import settings

# Create your models here.


class UserSite(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=511, blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.user}"


class BuyCar(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.CharField(max_length=511)
    cart_number = models.CharField(max_length=511)
    date = models.DateTimeField()
    max_price = models.PositiveBigIntegerField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.user}: {self.car} - {self.date}"