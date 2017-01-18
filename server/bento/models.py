from django.db import models
from django.utils.timezone import now


class Order(models.Model):
    """
        captcha: captcha驗證碼
        id: 身份證字號
        resNo: 訂位預約號
        ribsBox: 排骨便當數量
        vegetarianBox: 素食便當數量
        vat: 統一編號
    """
    id = models.CharField(max_length=10) # 身份證字號
    resNo = models.CharField(max_length=128, primary_key=True) # 訂位預約號
    ribsBox = models.PositiveIntegerField(default=0) # 排骨便當數量
    vegetarianBox = models.PositiveIntegerField(default=0) # 素食便當數量
    vat = models.CharField(max_length=8) # 統一編號

    created_at = models.DateTimeField(auto_now_add=True)
