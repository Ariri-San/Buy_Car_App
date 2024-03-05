from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework import status
from .models import BuyCar
from .serializers import CreateBuyCarSerializer, UpdateBuyCarSerializer, BuyCarSerializer

# Create your views here.


class BuyCarViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
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
