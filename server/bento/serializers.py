from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
        將Model轉換成可以serialize的資料
        也用來驗證輸入
        及存取Model
    """
    class Meta:
        model = Order
        fields = ("id", "resNo", "ribsBox", "vegetarianBox", "vat")
