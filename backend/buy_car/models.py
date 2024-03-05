from django.db import models
from django.conf import settings

# Create your models here.


class Car(models.Model):
    sites = [
        ('S', 'Saipa'),
        ('D', 'Dizel'),
    ]
    name = models.CharField(max_length=511)
    site = models.CharField(max_length=1, choices=sites)

    def __str__(self) -> str:
        return f"{self.site} : {self.name}"


class BuyCar(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    cart_number = models.CharField(max_length=511)
    date = models.DateTimeField()
    token_login = models.CharField(max_length=511, blank=True, null=True)
    max_price = models.PositiveBigIntegerField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.user} : {self.car.site} - {self.car.name} - {self.date.year}/{self.date.month}/{self.date.day} - {self.date.hour}:{self.date.minute}:{self.date.second}"



