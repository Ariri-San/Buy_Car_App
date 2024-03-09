from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy

# Create your models here.


class User(AbstractUser):
    username_site = models.CharField(gettext_lazy("National Code"), max_length=10, validators=[MinLengthValidator(10)], unique=True)
    password_site = models.CharField(max_length=127)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(blank=True, null=True)

