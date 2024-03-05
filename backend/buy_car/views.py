from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime, timedelta, timezone
import asyncio
from .app_selenium import send_images
from .models import BuyCar, Captcha
from .serializers import CreateBuyCarSerializer, UpdateBuyCarSerializer, BuyCarSerializer

# Create your views here.


class BuyCarViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return BuyCar.objects.all()
        return BuyCar.objects.filter(user=self.request.user).all()
    
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateBuyCarSerializer
        elif self.request.method == "PUT":
            return UpdateBuyCarSerializer
        return BuyCarSerializer
    
    
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'user': self.request.user
        }


class LoginUsers(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # try:
        start = datetime.today().replace(tzinfo=timezone.utc)
        finish = start + timedelta(hours=100)
        
        list_buy = BuyCar.objects.filter(date__gt=start, date__lte=finish).all()
        list_buy_serializer = BuyCarSerializer(data=list_buy, many=True)
        list_buy_serializer.is_valid()
        
        list_buy_cars = [buy_car.car.name for buy_car in list_buy]
        asyncio.run(send_images(list_buy_cars))
            
        # except:
        #     return Response(data={"comment": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if list_buy:
            return Response(
                data={
                    "comment": "success",
                    "start": start,
                    "finish": finish,
                    "list_buy": list_buy_serializer.data,
                    },
                status=status.HTTP_201_CREATED)
        return Response(data={"comment": "Not Found Request For Buy Car", "start": start, "finish": finish}, status=status.HTTP_200_OK)

