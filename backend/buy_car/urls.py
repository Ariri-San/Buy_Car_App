from rest_framework_nested import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register('buy_car', views.BuyCarViewSet, basename='buy_car')


api_urls = [
    path('login_users/', views.LoginUsers.as_view()),
]

urlpatterns = router.urls + api_urls