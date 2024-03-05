from rest_framework import serializers
from .models import BuyCar, Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['name', 'site', 'price']



class CreateBuyCarSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return BuyCar.objects.create(**validated_data, user=self.context["user"])
    
    class Meta:
        model = BuyCar
        fields = ['id', 'car', 'cart_number', 'date', 'max_price']


class UpdateBuyCarSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    
    class Meta:
        model = BuyCar
        fields = ['car', 'cart_number', 'date', 'max_price']


class BuyCarSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    
    class Meta:
        model = BuyCar
        fields = ['id', 'car', 'cart_number', 'date', 'max_price']
