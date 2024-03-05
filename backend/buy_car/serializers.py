from rest_framework import serializers
from .models import BuyCar


class CreateBuyCarSerializer(serializers.ModelSerializer):
    class Meta():
        model = BuyCar
        fields = ['id', 'username', 'password', 'phone', 'email']


class UpdateBuyCarSerializer(serializers.ModelSerializer):
    class Meta():
        model = BuyCar
        fields = ['id', 'username', 'password', 'phone', 'email']


class BuyCarSerializer(serializers.ModelSerializer):
    class Meta():
        model = BuyCar
        fields = ['id', 'username', 'password', 'phone', 'email']