from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy

# Create your models here.


class User(AbstractUser):
    username = models.CharField(gettext_lazy("National Code"), max_length=10, validators=[MinLengthValidator(10)], unique=True)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)

