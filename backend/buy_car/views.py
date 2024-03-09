from django.http import HttpResponseRedirect
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime, timedelta, timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
import asyncio
import time
from .app_selenium import get_captcha, check_login, login
from .models import BuyCar, Captcha
from .serializers import CreateBuyCarSerializer, UpdateBuyCarSerializer, BuyCarSerializer, SendCaptchaCode

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


options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
browser = webdriver.Chrome(options=options)
browser.get('https://esale.ikd.ir/login')


class LoginUsers(APIView):
    permission_classes = [IsAdminUser]
    
    
    def get(self, request):
        try:
            start = datetime.today().replace(tzinfo=timezone.utc)
            finish = start + timedelta(hours=100)
            
            list_buy = BuyCar.objects.filter(date__gt=start, date__lte=finish, token_login=None).all()
            
            list_buy_serializer = BuyCarSerializer(data=list_buy, many=True)
            list_buy_serializer.is_valid()
        except:
            return Response(data={"comment": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
        # list_buy_cars = [{
        #     "id":buy_car.car.id,
        #     "name":buy_car.car.name}
        #         for buy_car in list_buy]
        # results = asyncio.run(save_images(list_buy_cars))
        # print(results)
        
        # for buy_car in list_buy:
        #     save_image(buy_car)
        
            
        
        if list_buy:
            
            captch_image_element = browser.find_element(By.CSS_SELECTOR, "#root > div > div.wrapper.d-flex.flex-column.min-vh-100.bg-light > div.body.flex-grow-1.px-0 > div > div > div > div.row.justify-content-center > div > div > div.card.p-12 > div > form > div > div > div:nth-child(3) > div > span > img")
            get_captcha(browser, captch_image_element, './media/captcha/images/image.png', 98, 85, 1.4)
            
            return Response(
                data={
                    "comment": "success",
                    "link_image": request.build_absolute_uri("/media/captcha/images/image.png"),
                    "start": start,
                    "finish": finish,
                    "first_user":list_buy.first().user.username,
                    "first_id": list_buy.first().id,
                    "list_buy": list_buy_serializer.data,
                    },
                status=status.HTTP_201_CREATED)
        return Response(data={"comment": "Not Found Request For Buy Car", "start": start, "finish": finish}, status=status.HTTP_200_OK)


    def post(self, request):
        serializer_code = SendCaptchaCode(data=request.data)
        serializer_code.is_valid()
        
        buy_car = BuyCar.objects.get(id=serializer_code.data["id"])
        if_login = login(browser=browser, username=buy_car.user.username_site, password=buy_car.user.password_site, code=serializer_code.data["code"])
        
        if if_login:
            time.sleep(3)
            
            _, is_login = check_login(browser)
            
            if is_login:
                token = browser.execute_script("return window.localStorage.getItem(arguments[0]);", "SaleInternet")
                buy_car.token_login = token
                buy_car.save()
            
                browser.get('https://esale.ikd.ir/login')
                return HttpResponseRedirect("/login_users")
        
        return Response(data={"comment": "error"})
