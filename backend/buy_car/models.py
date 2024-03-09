from django.dispatch import receiver
from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator

# Create your models here.


class Car(models.Model):
    sites = [
        ('S', 'Saipa'),
        ('D', 'Dizel'),
    ]
    name = models.CharField(max_length=511)
    site = models.CharField(max_length=1, choices=sites)
    price = models.PositiveBigIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.site} : {self.name} - {self.price}$"


class BuyCar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    cart_number = models.CharField(max_length=16, validators=[MinLengthValidator(16)])
    date = models.DateTimeField()
    token_login = models.CharField(max_length=511, blank=True, null=True)
    max_price = models.PositiveBigIntegerField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.user} : {self.car.site} - {self.car.name} - {self.date.year}/{self.date.month}/{self.date.day} - {self.date.hour}:{self.date.minute}:{self.date.second}"


class HistoryBuyCar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    cart_number = models.CharField(max_length=16, validators=[MinLengthValidator(16)])
    date = models.DateTimeField()
    max_price = models.PositiveBigIntegerField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.user} : {self.car.site} - {self.car.name} - {self.date.year}/{self.date.month}/{self.date.day} - {self.date.hour}:{self.date.minute}:{self.date.second}"


class Captcha(models.Model):
    buy_car = models.ForeignKey(BuyCar, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="captcha/images", blank=True, null=True)
    text_captcha = models.CharField(max_length=63, blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.buy_car.user} : {self.buy_car.car}"

